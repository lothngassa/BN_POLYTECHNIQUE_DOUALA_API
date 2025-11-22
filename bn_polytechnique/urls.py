"""
URL configuration pour le projet bn_polytechnique.
"""
from django.contrib import admin
from django.urls import path, include
# Importations nécessaires pour servir les fichiers médias
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Route pour l'administration Django
    path('admin/', admin.site.urls),

    # Route principale pour l'API REST
    # TOUT le trafic vers /api/ sera géré par l'application 'memoires'
    path('api/', include('memoires.urls')),
]

# =========================================================
# Configuration pour servir les fichiers MÉDIAS (PDFs)
# =========================================================
# Cette ligne est essentielle pour que les URLs de fichiers PDF (MEDIA_URL) soient accessibles.
# Elle ne fonctionne correctement que lorsque DEBUG=True.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
