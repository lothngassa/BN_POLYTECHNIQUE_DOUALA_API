import logging
import time

from rest_framework import status, viewsets
from rest_framework.response import Response
from slugify import slugify

from .covers import first_page_jpeg
from .models import Memoire
from .permissions import LectureEtDepotPublics
from .serializers import MemoireSerializer
from .supabase_storage import upload_file

logger = logging.getLogger(__name__)

MAX_PDF_MB = 40


def _error(field, message, code=status.HTTP_400_BAD_REQUEST):
    return Response({field: [message]}, status=code)


class MemoireViewSet(viewsets.ModelViewSet):
    queryset = Memoire.objects.all()
    serializer_class = MemoireSerializer
    permission_classes = [LectureEtDepotPublics]

    def create(self, request, *args, **kwargs):
        """Dépôt d'un mémoire : on vérifie tout, puis on envoie le PDF et sa couverture au stockage."""
        pdf = request.FILES.get("fichier_pdf")
        if pdf is None:
            return _error("fichier_pdf", "Le fichier PDF est obligatoire.")
        if pdf.size > MAX_PDF_MB * 1024 * 1024:
            return _error("fichier_pdf", f"Le fichier dépasse {MAX_PDF_MB} Mo.")
        content = pdf.read()
        if not content.startswith(b"%PDF-"):
            return _error("fichier_pdf", "Le fichier doit être un PDF.")

        data = request.data.copy()
        for key in ("fichier_pdf", "couverture"):
            data.pop(key, None)
        if data.get("axe") and not data.get("axe_recherche"):  # ancien formulaire
            data["axe_recherche"] = data.get("axe")

        # 1. Valider les champs AVANT d'écrire quoi que ce soit dans le stockage
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 2. Envoyer le PDF, puis sa couverture (une couverture ratée ne bloque pas le dépôt)
        name = f"{slugify(serializer.validated_data['titre'])[:80] or 'memoire'}-{int(time.time())}"
        try:
            pdf_url = upload_file(content, f"pdfs/{name}.pdf", "application/pdf")
        except Exception:
            logger.exception("Échec de l'envoi du PDF")
            return _error("fichier_pdf", "Le stockage du fichier a échoué. Réessayez dans un instant.",
                          status.HTTP_503_SERVICE_UNAVAILABLE)
        cover_url = ""
        jpeg = first_page_jpeg(content)
        if jpeg:
            try:
                cover_url = upload_file(jpeg, f"couvertures/{name}.jpg", "image/jpeg")
            except Exception:
                logger.exception("Couverture non enregistrée")

        # 3. Enregistrer la fiche
        memoire = serializer.save(
            fichier_pdf=self._absolute(request, pdf_url),
            couverture=self._absolute(request, cover_url) if cover_url else "",
        )
        out = self.get_serializer(memoire)
        return Response(out.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(out.data))

    @staticmethod
    def _absolute(request, url):
        return url if url.startswith("http") else request.build_absolute_uri(url)
