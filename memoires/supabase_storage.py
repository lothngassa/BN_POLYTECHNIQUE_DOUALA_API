# memoires/supabase_storage.py (Version finale - Option A)

import os
from supabase import create_client, Client

# --- Récupération des clés ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME", "memoires") 

# --- Initialisation du client ---
if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: SUPABASE_URL ou SUPABASE_KEY sont manquants. L'upload échouera.")
    supabase = None
else:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Erreur d'initialisation Supabase: {e}")
        supabase = None


def upload_pdf_to_supabase(file, filename):
    """
    Envoie un fichier PDF dans le bucket Supabase.
    Retourne l'URL publique du fichier.
    """
    if supabase is None:
        raise ConnectionError("Le client Supabase n'est pas initialisé. Vérifiez les variables d'environnement.")

    file_bytes = file.read()
    path_in_bucket = f"pdfs/{filename}"

    supabase.storage.from_(BUCKET_NAME).upload(
        file=path_in_bucket,
        file_content=file_bytes,
        file_options={"content-type": "application/pdf"}
    )

    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{path_in_bucket}"
