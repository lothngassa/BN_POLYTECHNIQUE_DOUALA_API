# memoires/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MemoireSerializer
from .models import Memoire


# API pour lister et soumettre des mémoires
@api_view(['GET', 'POST'])
def memoire_list(request):
    # 1. Gérer la SOUMISSION (POST) pour la PAGE SOUMISSION
    if request.method == 'POST':
        serializer = MemoireSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Soumission réussie !"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 2. Gérer la CONSULTATION (GET) pour la PAGE PRINCIPALE
    elif request.method == 'GET':
        memoires = Memoire.objects.all()
        serializer = MemoireSerializer(memoires, many=True)
        return Response(serializer.data)
