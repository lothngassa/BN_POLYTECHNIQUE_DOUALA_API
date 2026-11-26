"""Envoi des fichiers : Supabase Storage en production, le disque local en développement."""
import os
from pathlib import Path

from django.conf import settings

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME", "memoires")

_client = None


def _supabase():
    global _client
    if _client is None and SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client

        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


def upload_file(data: bytes, path: str, content_type: str) -> str:
    """Enregistre `data` sous `path` et renvoie son adresse publique.

    Sans Supabase et en mode DEBUG, le fichier est écrit dans MEDIA_ROOT
    et l'adresse renvoyée est relative (/media/...)."""
    client = _supabase()
    if client is not None:
        client.storage.from_(BUCKET_NAME).upload(
            path=path, file=data, file_options={"content-type": content_type}
        )
        return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{path}"
    if settings.DEBUG:
        target = Path(settings.MEDIA_ROOT) / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return f"{settings.MEDIA_URL}{path}"
    raise ConnectionError("Stockage non configuré : définissez SUPABASE_URL et SUPABASE_KEY.")
