from rest_framework import serializers

from .models import Memoire

FILIERES = {"GIT", "GCI", "GPH", "GM", "GE", "GP", "GMP", "GAM", "QHSE", "MP"}


class MemoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memoire
        fields = [
            "id", "titre", "auteur", "matricule", "annee",
            "filiere", "axe_recherche", "mots_cles", "resume",
            "fichier_pdf", "couverture", "date_soumission",
        ]
        # Les fichiers sont envoyés au stockage par la vue, jamais saisis à la main
        read_only_fields = ["fichier_pdf", "couverture", "date_soumission"]

    def validate_annee(self, value):
        if not 1990 <= value <= 2100:
            raise serializers.ValidationError("Année de soutenance invalide.")
        return value

    def validate_filiere(self, value):
        if value not in FILIERES:
            raise serializers.ValidationError("Filière inconnue.")
        return value
