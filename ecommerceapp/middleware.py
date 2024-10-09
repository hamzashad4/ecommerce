from .models import Settings, Categories, Cart, CartItem, Brands
from django.http import HttpResponse;
from .views import *
from django.shortcuts import get_object_or_404;

class GeneralMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        session_key = request.session.session_key
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                count = cart.items.count()
                cart_items = cart.items.all()
            
                total = 0
                for item in cart_items:
                    total += CartItem.get_total_price(item)
                if total >= 1500:
                    shipping_charges = 0
                else:
                    shipping_charges = 100
                grand_total = total+shipping_charges 
            else:
                shipping_charges=0
                grand_total=0
                total = 0
                count = 0
        elif not session_key:
            shipping_charges=0
            grand_total=0
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
                if total > 1499:
                    shipping_charges = 0
                else:
                    shipping_charges = 100
                grand_total = total+shipping_charges 
            else:
                shipping_charges=0
                grand_total=0
                total = 0
                count = 0
            
        data = {
            "categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
            "brands": Brands.objects.all(),
            "cart_count": count,
            "total": total,
            "grand_total":grand_total,
            "shipping_charges":shipping_charges,
        }

        request.data = data
        response = self.get_response(request)
        return response