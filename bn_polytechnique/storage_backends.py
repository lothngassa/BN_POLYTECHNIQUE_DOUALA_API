# memoires/supabase_storage.py (Version simplifiée et fonctionnelle)

import os
from supabase import create_client, Client
from django.conf import settings # Maintenir l'import de settings est une bonne pratique

# Récupération des variables d'environnement (elles doivent être définies sur Render!)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME", "memoires") # Utilisez "memoires" par défaut si non défini

# Initialisation du client Supabase
if not SUPABASE_URL or not SUPABASE_KEY:
    # Ceci vous donnera une erreur claire au démarrage si les clés manquent
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

    # Lire le contenu du fichier
    file_bytes = file.read()

    # Le chemin et le nom que le fichier aura dans le bucket (ex: "pdfs/mon_memoire.pdf")
    path_in_bucket = f"pdfs/{filename}"

    # Upload direct vers Supabase Storage
    # Note: Dans la librairie Python Supabase, 'file' est le chemin dans le bucket, et 'file_content' est le contenu en octets.
    supabase.storage.from_(BUCKET_NAME).upload(
        file=path_in_bucket,
        file_content=file_bytes,
        file_options={"content-type": "application/pdf"}
    )

    # L'URL publique sera utilisée par votre frontend
    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{path_in_bucket}"
