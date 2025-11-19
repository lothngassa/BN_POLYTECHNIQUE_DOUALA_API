"""
URL configuration pour le projet bn_polytechnique.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Route pour l'administration Django
    path('admin/', admin.site.urls),

    # Route principale pour l'API REST
    # TOUT le trafic vers /api/ sera géré par l'application 'memoires'
    path('api/', include('memoires.urls')),
]

# Ajout des URLs pour servir les fichiers médias (PDFs) en mode DEV/Production
# Ceci est essentiel pour que les URLs de fichiers PDF (MEDIA_URL) soient accessibles
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# NOTE: Render (en mode production) n'utilise pas cette configuration pour les statics,
# mais elle est utile pour les fichiers MEDIA (PDFs) et la compatibilité.