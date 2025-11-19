from rest_framework import serializers
from .models import Memoire


class MemoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memoire
        # Assurez-vous que tous les champs de votre modèle sont listés ici
        fields = ['id', 'titre', 'auteur', 'annee', 'filiere', 'fichier_pdf']

        # --- LIGNE CLÉ AJOUTÉE POUR LE DÉPLOIEMENT/TEST ---
        # Ceci permet d'omettre le fichier PDF lors de la création d'un test
        extra_kwargs = {
            'fichier_pdf': {'required': False}
        }
        # ----------------------------------------------------