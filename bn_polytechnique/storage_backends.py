from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
import logging
import os # Ajout de l'importation de 'os' pour les chemins

logger = logging.getLogger(__name__)

# Créez une instance du client Supabase une seule fois pour la réutilisation
def get_supabase_client():
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    if not url or not key:
        logger.warning("Les variables d'environnement SUPABASE_URL ou SUPABASE_KEY sont manquantes.")
        return None
    
    try:
        # Initialisation du client Supabase
        supabase: Client = create_client(url, key)
        # Test de la connexion (optionnel mais utile)
        logger.info("Le client Supabase a été initialisé avec succès.")
        return supabase
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du client Supabase : {e}")
        return None

class SupabaseStorage(Storage):
    # L'URL de base où les fichiers sont servis, lue depuis settings.MEDIA_URL
    base_url = settings.MEDIA_URL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialisation du client lors de l'instanciation de la classe
        self.client = get_supabase_client()
        self.bucket_name = settings.SUPABASE_BUCKET_NAME.lower()

    def _save(self, name, content):
        if not self.client:
            raise Exception("Client Supabase non initialisé.")
        
        # Récupère le type de contenu (MIME type) du fichier
        file_content_type = getattr(content.file, 'content_type', 'application/octet-stream')

        try:
            # 🚨 CORRECTION CRITIQUE : Utiliser 'file=' au lieu de 'file_content='
            # Le client Python de Supabase s'attend au paramètre 'file'.
            res = self.client.storage.from_(self.bucket_name).upload(
                path=name,
                file=content.file,  # <-- FIX: Nous passons l'objet fichier directement.
                file_options={"content-type": file_content_type}
            )
            
            logger.info(f"Upload Supabase réussi. Résultat : {res}")
        except Exception as e:
            logger.error(f"Erreur lors de l'upload Supabase pour {name} : {e}")
            # L'erreur sera relancée par Django, affichant le 500
            raise 

        # Retourne le nom du fichier sous lequel il a été stocké
        return name

    def _open(self, name, mode='rb'):
        # La lecture n'est pas implémentée pour l'instant.
        raise NotImplementedError("La lecture de fichier n'est pas implémentée dans ce stockage.")

    def exists(self, name):
        # Vérifie si un fichier existe
        if not self.client:
            return False
            
        try:
            # Tente de lister le fichier
            res = self.client.storage.from_(self.bucket_name).list(path=os.path.dirname(name), options={'search': os.path.basename(name)})
            # Vérifie si la réponse contient le nom de fichier recherché
            return any(item.get('name') == os.path.basename(name) for item in res)
        except Exception as e:
            logger.warning(f"Erreur lors de la vérification de l'existence du fichier {name}: {e}")
            return False

    def url(self, name):
        # Renvoie l'URL publique du fichier
        return os.path.join(self.base_url, name)
