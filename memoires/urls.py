from rest_framework.routers import DefaultRouter
from .views import MemoireViewSet
from django.urls import path, include

# Création du routeur DRF
router = DefaultRouter()
router.register(r'memoires', MemoireViewSet)

urlpatterns = [
    # Inclut toutes les routes générées par le ViewSet (GET, POST, PUT, DELETE)
    path('', include(router.urls)),
]
