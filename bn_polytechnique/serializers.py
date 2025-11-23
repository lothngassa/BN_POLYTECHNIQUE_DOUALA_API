from rest_framework import serializers
from .models import Memoire

class MemoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memoire
        fields = "__all__"
