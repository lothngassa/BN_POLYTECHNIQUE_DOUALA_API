# bn_polytechnique/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# NOTE : La ligne "from . import views" a été supprimée !

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirige /api/ vers les URLs de l'application memoires
    path('api/', include('memoires.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)