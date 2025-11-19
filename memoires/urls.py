from django.urls import path
from .views import MemoireListCreate

urlpatterns = [
    # Route pour lister et créer un mémoire
    # L'URL complète sera : /api/memoires/
    path('memoires/', MemoireListCreate.as_view(), name='memoire-list-create'),
]