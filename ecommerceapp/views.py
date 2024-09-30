from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required



def index(request): 
    feature_products = Products.objects.filter(is_feature =True, is_active =True).order_by('-created_at')
    trending_products = Products.objects.filter(is_trending =True, is_active =True).order_by('-created_at')
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
               'featured':feature_products,
               'trending':trending_products,
               "title":"Organic Grocery"
               }
    return render(request, 'ecommerceapp/index.html',context)

def errorpage(request):
    settings = Settings.objects.first()
    brands = Brands.objects.all()  
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
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
     
def cart(request):
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
                "title":"Cart"
               }
    return render(request, 'ecommerceapp/cart.html', context)

def checkout(request):
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
                "title":"Check Out",
               }
    return render(request, 'ecommerceapp/checkout.html', context)

def contact(request):
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
                "title":"Contact Us",
               }
    return render(request, 'ecommerceapp/contact.html', context)

@login_required
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
        'related_prods':related_prods,
        "title":"Product",
    }
    return render(request, 'ecommerceapp/single-product.html', context)