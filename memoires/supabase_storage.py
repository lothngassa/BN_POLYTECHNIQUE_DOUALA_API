# memoires/supabase_storage.py (MODIFICATION)

import os
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions # NOUVEL IMPORT


# --- Initialisation du client ---
# ... (le code if not SUPABASE_URL or not SUPABASE_KEY: reste le même)
else:
    try:
        # Tente l'initialisation
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test de connexion simple : Tentative d'accès à un bucket
        supabase.storage.from_(BUCKET_NAME).list() # <-- Ceci va lever une erreur si la clé est mauvaise !
        print("INFO: Le client Supabase a été initialisé avec succès et la connexion au bucket fonctionne.") # NOUVEAU LOG SUCCÈS
        
    except Exception as e:
        # Affiche l'ERREUR COMPLÈTE
        print("FATAL ERROR: ERREUR CRITIQUE lors de l'initialisation de Supabase.") # NOUVEAU LOG ERREUR
        print(f"DÉTAILS DE L'ERREUR : {e}")
        supabase = None
