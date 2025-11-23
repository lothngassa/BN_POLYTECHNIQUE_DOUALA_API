import os
from io import BytesIO

from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client

class SupabaseStorage(Storage):
    """
    Système de stockage personnalisé pour Supabase Storage.
    """
    def __init__(self, location=None, bucket_name=None, base_url=None):
        # Récupération des variables d'environnement
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.bucket_name: str = os.environ.get("SUPABASE_BUCKET_NAME")

        if not self.url or not self.key or not self.bucket_name:
            raise EnvironmentError("Les variables SUPABASE_URL, SUPABASE_KEY et SUPABASE_BUCKET_NAME doivent être définies.")

        # Initialisation du client Supabase
        self.supabase: Client = create_client(self.url, self.key)

        # Assurez-vous que la clé (Bucket Name) est en minuscules (bonne pratique Supabase)
        self.bucket_name = self.bucket_name.lower()
        self.base_url = f"{self.url}/storage/v1/object/public/{self.bucket_name}/"


    def _save(self, name, content):
        """
        Enregistre le fichier dans Supabase Storage.
        'name' est le chemin du fichier (ex: 'pdfs/monfichier.pdf').
        'content' est l'objet fichier de Django.
        """
        
        # Le contenu doit être un objet bytes
        if hasattr(content, 'read'):
            # Si c'est un fichier, lisez tout le contenu
            file_data = content.read()
        else:
            # Sinon, supposez que c'est déjà des bytes
            file_data = content

        # Upload vers Supabase
        try:
            # La méthode upload_from_file est plus simple mais peut échouer.
            # Ici, nous utilisons l'upload d'octets bruts:
            self.supabase.storage.from_(self.bucket_name).upload(
                file=file_data,
                path=name,
                file_options={"content-type": content.content_type if hasattr(content, 'content_type') else 'application/octet-stream'}
            )
        except Exception as e:
            # Supabase peut renvoyer un 409 (Conflict) si le fichier existe déjà. 
            # Dans ce cas, nous tentons un 'update'
            if "The resource already exists" in str(e):
                 self.supabase.storage.from_(self.bucket_name).update(
                    file=file_data,
                    path=name,
                    file_options={"content-type": content.content_type if hasattr(content, 'content_type') else 'application/octet-stream'}
                )
            else:
                raise e
            

        return name

    def _open(self, name, mode='rb'):
        """
        Ouvre un fichier pour la lecture (non essentiel pour l'accès public, mais requis par Django).
        """
        # Récupère l'objet bytes du fichier de Supabase
        res = self.supabase.storage.from_(self.bucket_name).download(name)
        
        # Renvoie le contenu sous forme de fichier en mémoire
        return BytesIO(res)

    def exists(self, name):
        """
        Vérifie si le fichier existe (non essentiel, mais utile).
        """
        try:
            self.supabase.storage.from_(self.bucket_name).get_public_url(name)
            return True
        except:
            return False

    def url(self, name):
        """
        Renvoie l'URL publique pour accéder directement au fichier.
        """
        # Supabase a une structure d'URL prévisible pour les buckets publics
        return self.base_url + name
        
    def delete(self, name):
        """
        Supprime le fichier.
        """
        self.supabase.storage.from_(self.bucket_name).remove([name])
