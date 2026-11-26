from django.contrib import admin

from .models import Memoire


@admin.register(Memoire)
class MemoireAdmin(admin.ModelAdmin):
    list_display = ("titre", "auteur", "filiere", "annee", "date_soumission")
    list_filter = ("filiere", "annee")
    search_fields = ("titre", "auteur", "matricule", "mots_cles")
