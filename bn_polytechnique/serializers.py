# memoires/serializers.py

from rest_framework import serializers
from .models import Memoire

class MemoireSerializer(serializers.ModelSerializer):
    """
    Définit la manière dont le modèle Memoire est converti en JSON.
    """
    class Meta:
        model = Memoire
        # Inclure tous les champs du modèle (titre, auteur, fichier_pdf, etc.)
        fields = '__all__'