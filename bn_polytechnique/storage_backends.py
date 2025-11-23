from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
import logging
import os 

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
        
        file_content_type = getattr(content.file, 'content_type', 'application/octet-stream')

        try:
            # FIX CRITIQUE : Utiliser 'file=' (argument attendu par la librairie Supabase)
            res = self.client.storage.from_(self.bucket_name).upload(
                path=name,
                file=content.file,  # L'OBJET FICHIER
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
