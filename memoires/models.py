# memoires/models.py

from django.db import models

class Memoire(models.Model):
    """
    Modèle de base pour enregistrer les mémoires de fin d'études.
    """
    # Données du formulaire
    titre = models.CharField(max_length=255, verbose_name="Titre du Mémoire")
    auteur = models.CharField(max_length=150, verbose_name="Nom(s) de l'Auteur(s)")
    annee = models.IntegerField(verbose_name="Année de Soutenance")

    # Pour le filtrage (selon votre code HTML)
    filiere = models.CharField(max_length=50, verbose_name="Filière (Ex: GI, GM, GC)")
    axe_recherche = models.CharField(max_length=100, blank=True, null=True, verbose_name="Axe de Recherche")

    # Champ clé pour le fichier PDF lui-même
    fichier_pdf = models.FileField(upload_to='memoires/pdfs/', verbose_name="Fichier PDF")

    # Champs automatiques
    date_soumission = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_soumission']

    def __str__(self):
        return f"{self.titre} par {self.auteur} ({self.annee})"
