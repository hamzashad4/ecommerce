from .models import Settings, Categories, Cart, CartItem, Brands
from django.http import HttpResponse;
from django.shortcuts import get_object_or_404;

class GeneralMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        session_key = request.session.session_key
        if not session_key:
            count = 0
            total = 0
        else:
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart:
                count = cart.items.count()
                cart_items = cart.items.all()
            
                total = 0
                for item in cart_items:
                    total += CartItem.get_total_price(item)
            else:
                total = 0
                count = 0
            
        data = {
            "categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
            "brands": Brands.objects.all(),
            "cart_count": count,
            "total": total
        }

        request.data = data
        response = self.get_response(request)
        return response