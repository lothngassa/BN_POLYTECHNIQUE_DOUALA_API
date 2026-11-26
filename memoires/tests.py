from unittest import mock

import pymupdf
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from .models import Memoire

URL = "/api/memoires/"


def make_pdf() -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Mémoire de test")
    data = doc.tobytes()
    doc.close()
    return data


def fake_upload(data, path, content_type):
    return f"https://stockage.test/{path}"


class MemoireApiTests(APITestCase):
    def payload(self, **extra):
        data = {
            "titre": "Un titre", "auteur": "Auteur", "matricule": "21G00001", "annee": 2025,
            "filiere": "GIT", "axe_recherche": "IA", "mots_cles": "a, b", "resume": "Résumé.",
            "fichier_pdf": SimpleUploadedFile("m.pdf", make_pdf(), content_type="application/pdf"),
        }
        data.update(extra)
        return data

    def test_list_is_public(self):
        self.assertEqual(self.client.get(URL).status_code, 200)

    @mock.patch("memoires.views.upload_file", side_effect=fake_upload)
    def test_submit_stores_pdf_and_cover(self, _upload):
        r = self.client.post(URL, self.payload(), format="multipart")
        self.assertEqual(r.status_code, 201, r.content)
        self.assertTrue(r.data["fichier_pdf"].endswith(".pdf"))
        self.assertTrue(r.data["couverture"].endswith(".jpg"))
        self.assertEqual(r.data["matricule"], "21G00001")

    def test_submit_requires_pdf(self):
        r = self.client.post(URL, self.payload(fichier_pdf=""), format="multipart")
        self.assertEqual(r.status_code, 400)

    def test_submit_rejects_non_pdf(self):
        bad = SimpleUploadedFile("m.pdf", b"not a pdf", content_type="application/pdf")
        r = self.client.post(URL, self.payload(fichier_pdf=bad), format="multipart")
        self.assertEqual(r.status_code, 400)

    @mock.patch("memoires.views.upload_file", side_effect=fake_upload)
    def test_invalid_fields_upload_nothing(self, upload):
        r = self.client.post(URL, self.payload(filiere="XYZ"), format="multipart")
        self.assertEqual(r.status_code, 400)
        upload.assert_not_called()

    def test_anonymous_cannot_delete_or_edit(self):
        m = Memoire.objects.create(titre="T", auteur="A", annee=2024, filiere="GIT", fichier_pdf="https://x.test/a.pdf")
        self.assertEqual(self.client.delete(f"{URL}{m.id}/").status_code, 403)
        self.assertEqual(self.client.patch(f"{URL}{m.id}/", {"titre": "X"}).status_code, 403)
        self.assertTrue(Memoire.objects.filter(id=m.id).exists())

    def test_staff_can_delete(self):
        m = Memoire.objects.create(titre="T", auteur="A", annee=2024, filiere="GIT", fichier_pdf="https://x.test/a.pdf")
        self.client.force_authenticate(User.objects.create_user("admin", is_staff=True))
        self.assertEqual(self.client.delete(f"{URL}{m.id}/").status_code, 204)
