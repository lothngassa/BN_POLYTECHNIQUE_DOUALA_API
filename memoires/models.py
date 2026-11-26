from django.db import models


class Memoire(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=150)
    matricule = models.CharField(max_length=30, blank=True, default="")
    annee = models.IntegerField()
    filiere = models.CharField(max_length=50)
    axe_recherche = models.CharField(max_length=100, blank=True, null=True)
    mots_cles = models.CharField(max_length=300, blank=True, default="")
    resume = models.TextField(blank=True, default="")

    # Adresses publiques des fichiers (Supabase Storage en production)
    fichier_pdf = models.URLField(max_length=500)
    couverture = models.URLField(max_length=500, blank=True, default="")

    date_soumission = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_soumission"]

    def __str__(self):
        return f"{self.titre} par {self.auteur} ({self.annee})"
