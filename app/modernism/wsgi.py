import os

from django.core.wsgi import get_wsgi_application

env = os.environ.copy()

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    env.get("DJANGO_SETTINGS_MODULE", "modernism.settings.dev"),
)

application = get_wsgi_application()
