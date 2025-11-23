from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
import logging
import os
import io 

logger = logging.getLogger(__name__)

def get_supabase_client():
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    if not url or not key:
        logger.warning("Les variables d'environnement SUPABASE_URL ou SUPABASE_KEY sont manquantes.")
        return None
    
    try:
        supabase: Client = create_client(url, key)
        logger.info("Le client Supabase a été initialisé avec succès.")
        return supabase
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du client Supabase : {e}")
        return None

class SupabaseStorage(Storage):
    base_url = settings.MEDIA_URL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = get_supabase_client()
        self.bucket_name = settings.SUPABASE_BUCKET_NAME.lower()

    def _save(self, name, content):
        if not self.client:
            raise Exception("Client Supabase non initialisé.")
        
        # CORRECTIF DÉFINITIF (tentative 3) : Utilisation de l'argument positionnel pour le contenu.
        
        # S'assurer que le pointeur de fichier est au début
        content.seek(0)
        file_bytes = content.read() # Lecture du contenu en mémoire (bytes)
        
        # Récupération du type de contenu
        file_content_type = getattr(content, 'content_type', 'application/octet-stream')
        
        try:
            # ATTENTION : on place 'file_bytes' en PREMIER argument, sans mot-clé (argument positionnel)
            res = self.client.storage.from_(self.bucket_name).upload(
                file_bytes, # CONTENU DU FICHIER EN BYTES
                path=name,  # L'argument 'path' est le second
                file_options={"content-type": file_content_type}
            )
            
            logger.info(f"Upload Supabase réussi. Résultat : {res}")
        except Exception as e:
            logger.error(f"Erreur lors de l'upload Supabase pour {name} : {e}")
            raise 

        return name

    def _open(self, name, mode='rb'):
        raise NotImplementedError("La lecture de fichier n'est pas implémentée dans ce stockage.")

    def exists(self, name):
        if not self.client:
            return False
            
        try:
            res = self.client.storage.from_(self.bucket_name).list(path=os.path.dirname(name), options={'search': os.path.basename(name)})
            return any(item.get('name') == os.path.basename(name) for item in res)
        except Exception as e:
            logger.warning(f"Erreur lors de la vérification de l'existence du fichier {name}: {e}")
            return False

    def url(self, name):
        return os.path.join(self.base_url, name)
