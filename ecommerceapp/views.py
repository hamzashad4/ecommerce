from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone



def index(request): 
    feature_products = Products.objects.filter(is_feature =True, is_active =True).order_by('-created_at')
    trending_products = Products.objects.filter(is_trending =True, is_active =True).order_by('-created_at')
    deal = Deal.objects.filter(is_active=True).first()
    percentage = ((((deal.product.price-deal.product.discount_price))/(deal.product.price))*100).__round__(2)

    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
               'featured':feature_products,
               'trending':trending_products,
               "title":"Organic Grocery",
               "deal":deal,
               "percentage":percentage,
               }
    return render(request, 'ecommerceapp/index.html',context)

def errorpage(request):


    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(),
                "title":"Error Page" 
               }
    return render(request, 'ecommerceapp/404.html', context)

def about(request):
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
                "title":"About Us"
               }
    return render(request, 'ecommerceapp/about.html', context)


def get_or_create_cart(request):
    session_key = request.session.session_key
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    return cart
     
def cart(request):
    if(request.data["cart_count"] > 0):
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()

    
        context ={
                    "shipping_charges":request.data["shipping_charges"],
                    "grand_total":request.data["grand_total"],
                    "total": request.data["total"],
                    "cart_items": cart_items,
                    "categories": Categories.objects.all(),
                    "settings": Settings.objects.first(),
                    "brands": Brands.objects.all(), 
                    "title":"Cart",
                    "count": request.data["cart_count"],
                    }
        return render(request, 'ecommerceapp/cart.html', context)
    else:
        messages.add_message(request, messages.ERROR, "Cart is empty!!")
        return redirect('ecommerceapp-home')

def add_to_cart(request, product_id):
    product = Products.objects.filter(id=product_id).first()
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get("quantity", 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, cost=product.cost_price, price=product.price)
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    messages.add_message(request, messages.SUCCESS, "Product added to Cart")
    return redirect('ecommerceapp-home')

def delete_cart_item(request, item_id):
    cart_item = CartItem.objects.filter(id=item_id).first()
    cart_item.delete()
    
    messages.add_message(request, messages.SUCCESS, "Cart Item Deleted Successfully...")
    return redirect('ecommerceapp-cart')

def update_cart_item(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist("cart_item_ids")
        quantities = request.POST.getlist("quantities")

        for item_id, quantity in zip(item_ids, quantities):
            quantity = int(quantity)
            if quantity > 0:
                cart_item = CartItem.objects.filter(id=item_id).first()
                cart_item.quantity = quantity
                cart_item.save()
            else:
                CartItem.objects.filter(id=item_id).delete()
        messages.add_message(request, messages.SUCCESS, "Cart updated successfully...")

    return redirect('ecommerceapp-cart')

def checkout(request):
    if(request.data["cart_count"]> 0):
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()   

        context ={
            "shipping_charges":request.data["shipping_charges"],
            "grand_total":request.data["grand_total"],
            "total": request.data["total"],
            "cart_items": cart_items,
            "categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
            "brands": Brands.objects.all(), 
            "title":"Check Out",
            "count": request.data["cart_count"],
                }
        return render(request, 'ecommerceapp/checkout.html', context)
    else:
        messages.add_message(request, messages.ERROR, "Cart is empty!!")
        return redirect('website-home')
    
def placeOrder(request):
    if request.method == "POST":
       cart = get_or_create_cart(request)
       
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       email = request.POST.get('email')
       phone = request.POST.get('phone')
       country = request.POST.get('country')
       city = request.POST.get('city')
       zip = request.POST.get('zip')
       address = request.POST.get('address')
       note = request.POST.get('note')
       payment = request.POST.get('peyment')
       order = models.Order.objects.create(cart_id=cart.id, first_name=first_name, last_name=last_name, email=email, phone=phone, country=country, city=city, zip=zip, note=note, address=address, payment=payment, total=request.data["total"])
       
       request.session.flush() #to delete session key from session
       
       messages.add_message(request, messages.SUCCESS, f"Your order has been placed! Order # {order.id}")
       return redirect('ecommerceapp-home')

def contact(request):
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
                "title":"Contact Us",
               }
    return render(request, 'ecommerceapp/contact.html', context)

@login_required(login_url='/accounts/')
def news(request):
    settings = Settings.objects.all().first()   
    context ={
               'settings': settings,
               }
    return render(request, 'ecommerceapp/news.html', context)

def shop(request):
    products = Products.objects.filter(is_active=True).order_by('-id')
        

    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
               'products':products,
               "title":"Shop"
               }
    return render(request, 'ecommerceapp/shop.html' ,context)

def shop_category(request, category_id):
    products = Products.objects.filter(category_id=category_id, is_active=True)
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
               'products':products,
               "title":"Shop"
               }
    return render(request, 'ecommerceapp/shop.html' ,context)

def shop_search(request):
    query = request.GET.get('search')
    products = Products.objects.filter(name__icontains=query, is_active=True)
    context ={"categories": Categories.objects.all(),
                "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
               'products':products,
               "title":"Shop",
               }
    return render(request, 'ecommerceapp/shop.html' ,context)

def single_news(request):
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(),
                "title":"News", 
               }
    return render(request, 'ecommerceapp/single-news.html', context)

def single_product(request, id):
    products = Products.objects.filter(id=id).first()
    related_prods = Categories.objects.get(id=products.category_id).products.filter(is_active=True)
    

    context={
        "categories": Categories.objects.all(),
        "settings": Settings.objects.first(),
        "brands": Brands.objects.all(), 
        "products":products,
        'related_prods':related_prods,
        "title":"Product",
    }
    return render(request, 'ecommerceapp/single-product.html', context)