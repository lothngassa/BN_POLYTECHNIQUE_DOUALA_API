# memoires/supabase_storage.py (VERSION CORRIGÉE ET DÉBOGUÉE)

import os
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions # Import nécessaire si on utilise des options, mais gardé pour la propreté

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
        # 1. Tente l'initialisation
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 2. Test de connexion au bucket (pour forcer un message d'erreur clair si la clé est invalide)
        supabase.storage.from_(BUCKET_NAME).list() 
        print("INFO: Le client Supabase a été initialisé avec succès et la connexion au bucket fonctionne.")
        
    except Exception as e:
        # Affiche l'ERREUR CRITIQUE pour le débogage Render
        print("FATAL ERROR: ERREUR CRITIQUE lors de l'initialisation de Supabase.")
        print(f"DÉTAILS DE L'ERREUR : {e}")
        supabase = None


def upload_pdf_to_supabase(file, filename):
    """
    Envoie un fichier PDF dans le bucket Supabase.
    Retourne l'URL publique du fichier.
    """
    if supabase is None:
        raise ConnectionError("Le client Supabase n'est pas initialisé. Vérifiez les variables d'environnement et les logs d'erreurs FATAL.")

    file_bytes = file.read()
    # Le chemin dans le bucket sera 'pdfs/nomdufichier.pdf'
    path_in_bucket = f"pdfs/{filename}"

    supabase.storage.from_(BUCKET_NAME).upload(
        file=path_in_bucket,
        file_content=file_bytes,
        file_options={"content-type": "application/pdf"}
    )

    # Retourne l'URL publique complète
    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{path_in_bucket}"
