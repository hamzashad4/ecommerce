import os
from django.core.asgi import get_asgi_application
from mangum import Mangum

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

# Get the ASGI application
django_app = get_asgi_application()

# Create the Mangum handler
handler = Mangum(django_app)
