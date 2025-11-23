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
        logger.warning("Supabase config missing.")
        return None
    try:
        return create_client(url, key)
    except Exception as e:
        logger.error(f"Supabase init error: {e}")
        return None

class NewSupabaseStorage(Storage):
    base_url = settings.MEDIA_URL

    def __init__(self, *args, **kwargs):
        self.client = get_supabase_client()
        self.bucket_name = settings.SUPABASE_BUCKET_NAME.lower()

    def _save(self, name, content):
        if not self.client:
            raise Exception("Supabase client not ready.")

        # Lecture du contenu
        content.seek(0)
        file_bytes = content.read()
        file_content_type = getattr(content, 'content_type', 'application/octet-stream')

        try:
            # --- LE CORRECTIF EST ICI ---
            # On utilise 'data' et on passe les bytes
            self.client.storage.from_(self.bucket_name).upload(
                path=name,
                file=file_bytes, # Argument correct pour la librairie récente
                file_options={"content-type": file_content_type}
            )
            logger.info(f"Upload OK: {name}")
        except Exception as e:
            # Si l'upload échoue, on log l'erreur mais on laisse Django gérer
            logger.error(f"Upload failed: {e}")
            raise e

        return name

    def _open(self, name, mode='rb'):
        raise NotImplementedError("Not implemented")

    def exists(self, name):
        if not self.client: return False
        try:
            res = self.client.storage.from_(self.bucket_name).list(
                path=os.path.dirname(name), 
                options={'search': os.path.basename(name)}
            )
            return any(item.get('name') == os.path.basename(name) for item in res)
        except:
            return False

    def url(self, name):
        return os.path.join(self.base_url, name)
