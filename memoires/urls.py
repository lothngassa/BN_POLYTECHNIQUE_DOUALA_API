# memoires/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('memoires/', views.memoire_list, name='memoire-list-submit'),
]