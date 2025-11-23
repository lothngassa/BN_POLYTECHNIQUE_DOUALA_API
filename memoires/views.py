from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Memoire
from .serializers import MemoireSerializer
from .supabase_storage import upload_pdf_to_supabase
import logging
from django.core.files.uploadedfile import UploadedFile

logger = logging.getLogger(__name__)

class MemoireViewSet(viewsets.ModelViewSet):
    queryset = Memoire.objects.all()
    serializer_class = MemoireSerializer

    def create(self, request, *args, **kwargs):
        """
        Gère la création d'un nouveau mémoire, y compris l'upload
        du fichier PDF vers Supabase.
        """
        # 1. Extraction des données (y compris le fichier)
        data = request.data.copy()
        pdf_file = data.pop('fichier_pdf', [None])[0] # Extrait le fichier_pdf

        # Vérification si un fichier a été soumis
        if not pdf_file or not isinstance(pdf_file, UploadedFile):
            logger.error("Aucun fichier PDF trouvé ou le format est incorrect.")
            # Si le fichier est manquant, on renvoie une erreur 400 personnalisée.
            return Response(
                {"fichier_pdf": ["Le fichier PDF est obligatoire."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Préparation du nom de fichier
        # On utilise le titre pour garantir un nom de fichier unique et lisible.
        # Vous pouvez ajuster cela.
        if 'titre' in data and data['titre']:
            import slugify # Assurez-vous d'avoir 'python-slugify' installé
            file_slug = slugify.slugify(data['titre'])
        else:
            file_slug = pdf_file.name.split('.')[0]

        # On ajoute un timestamp pour garantir l'unicité
        import time
        filename = f"{file_slug}-{int(time.time())}.pdf"

        # 3. Upload vers Supabase et récupération de l'URL
        try:
            # L'upload doit se faire AVANT la validation du sérialiseur
            pdf_url = upload_pdf_to_supabase(pdf_file, filename)
            logger.info(f"Fichier uploadé avec succès. URL: {pdf_url}")

            # 4. Injection de l'URL dans les données pour la validation DB
            # Le sérialiseur s'attend maintenant à une URL valide, et non au fichier brut.
            data['fichier_pdf'] = pdf_url

        except Exception as e:
            logger.error(f"Échec de l'upload vers Supabase: {e}")
            return Response(
                {"fichier_pdf": [f"Erreur d'upload vers le stockage: {e}"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 5. Validation et Sauvegarde dans la Base de Données
        serializer = self.get_serializer(data=data)

        # Si le sérialiseur échoue ici, c'est que les autres champs (titre, auteur, etc.)
        # ont un problème de validation.
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 6. Réponse de succès
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

# Vous pouvez ajouter d'autres vues ici si nécessaire
