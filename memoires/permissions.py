from rest_framework.permissions import SAFE_METHODS, BasePermission


class LectureEtDepotPublics(BasePermission):
    """Tout le monde peut consulter et déposer un mémoire.

    Modifier ou supprimer est réservé à l'équipe (comptes is_staff de l'admin Django)."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "POST":
            return True
        return bool(request.user and request.user.is_staff)
