"""
WSGI config for bn_polytechnique project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bn_polytechnique.settings')

application = get_wsgi_application()


def _migrate_on_render():
    """Sur Render, applique les migrations au démarrage : la base suit toujours le code.

    Un verrou PostgreSQL évite que deux processus migrent en même temps.
    Sans migration en attente, l'opération ne fait rien."""
    from django.core.management import call_command
    from django.db import connection

    if connection.vendor != "postgresql":
        call_command("migrate", interactive=False, verbosity=0)
        return
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_advisory_lock(726312)")
        try:
            call_command("migrate", interactive=False, verbosity=0)
        finally:
            cursor.execute("SELECT pg_advisory_unlock(726312)")


if os.environ.get("RENDER"):
    _migrate_on_render()
