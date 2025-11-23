# memoires/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MemoireSerializer
from .models import Memoire

# IMPORTANT : Assurez-vous d'avoir ce fichier dans votre app 'memoires'
from .supabase_storage import upload_pdf_to_supabase 


# API pour lister et soumettre des mémoires
@api_view(['GET', 'POST'])
def memoire_list(request):
    
    # 1. Gérer la SOUMISSION (POST) pour la PAGE SOUMISSION
    if request.method == 'POST':
        # Le fichier est extrait de request.FILES avant la sérialisation
        pdf_file = request.FILES.get("fichier_pdf") 
        
        # Vérification si un fichier est présent (cause fréquente de 400)
        if not pdf_file:
            return Response({"error": "Fichier PDF requis ('fichier_pdf' manquant)."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Upload du fichier vers Supabase
            pdf_url = upload_pdf_to_supabase(pdf_file, pdf_file.name)
            
            # 2. Création des données pour le serializer
            # Nous utilisons une copie modifiable des données de la requête
            data_mutable = request.data.copy()
            # On remplace l'objet fichier par l'URL publique générée
            data_mutable['fichier_pdf'] = pdf_url

            # 3. Sérialisation des données
            serializer = MemoireSerializer(data=data_mutable)

            if serializer.is_valid():
                # 4. Sauvegarde de l'objet Memoire avec l'URL dans le champ fichier_pdf (URLField)
                serializer.save()
                return Response({"message": "Soumission réussie !", "data": serializer.data}, status=status.HTTP_201_CREATED)
            
            # Si le serializer n'est pas valide (champs manquants, etc.)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Gérer les erreurs liées à l'upload Supabase ou autres
            print(f"Erreur lors de l'upload ou de la sauvegarde: {e}")
            return Response({"error": "Erreur serveur lors du traitement du fichier.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 2. Gérer la CONSULTATION (GET) pour la PAGE PRINCIPALE
    elif request.method == 'GET':
        memoires = Memoire.objects.all()
        serializer = MemoireSerializer(memoires, many=True)
        return Response(serializer.data)
