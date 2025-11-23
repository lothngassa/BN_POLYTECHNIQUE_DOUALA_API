from rest_framework import serializers
from .models import Memoire

class MemoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memoire
        fields = [
            'id', 'titre', 'auteur', 'annee',
            'filiere', 'axe_recherche',
            'fichier_pdf', 'date_soumission'
        ]

        extra_kwargs = {
            'fichier_pdf': {'required': True}   # il FAUT un fichier
        }
