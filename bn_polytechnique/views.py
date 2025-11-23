from django.http import JsonResponse

def api_root_view(request):
    """
    Vue de la racine de l'API. Elle retourne un statut simple 200 OK
    pour les contrôles de santé de Render et fournit les endpoints disponibles.
    """
    return JsonResponse({
        "status": "API du BN Polytechnique est opérationnelle",
        "message": "Bienvenue sur l'API. Consultez l'endpoint /API/memoires/ pour les thèses.",
        "endpoints": {
            "memoires": "/API/memoires/"
        }
    })
