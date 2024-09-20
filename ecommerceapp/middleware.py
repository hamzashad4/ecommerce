from .models import *


class GeneralMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.settings = Settings.objects.all().first()
        request.brands = Brands.objects.all()  

        response = self.get_response(request)
        return response
