from django.shortcuts import render
from django.http import HttpResponse
from .models import *



def index(request): 
    feature_products = Products.objects.filter(is_feature =True, is_active =True).order_by('-created_at')
    trending_products = Products.objects.filter(is_trending =True, is_active =True).order_by('-created_at')
    settings = Settings.objects.first()
    brands = Brands.objects.all()
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    context ={'categories':categories,
               'sub_categories':sub_categories,
               'settings':settings,
               'brands': brands,
               'featured':feature_products,
               'trending':trending_products,
               }
    return render(request, 'ecommerceapp/index.html',context)

def errorpage(request):
    settings = Settings.objects.first()
    brands = Brands.objects.all()  
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    context ={'categories':categories,
               'sub_categories':sub_categories,
               'settings':settings,
               'brands': brands,
               }
    return render(request, 'ecommerceapp/404.html', context)

def about(request):
    settings = Settings.objects.first()
    brands = Brands.objects.all()
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    context ={'categories':categories,
               'sub_categories':sub_categories,
               'settings':settings,
               'brands': brands,
               }
    return render(request, 'ecommerceapp/about.html', context)
     
def cart(request):
    settings = Settings.objects.all().first()
    brands = Brands.objects.all()   
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    context ={'categories':categories,
               'sub_categories':sub_categories,
               'brands':brands,
               'settings': settings
               }
    return render(request, 'ecommerceapp/cart.html', context)

def checkout(request):
    settings = Settings.objects.all().first()
    brands = Brands.objects.all()   
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    context ={'categories':categories,
               'sub_categories':sub_categories,
               'brands':brands,
               'settings': settings
               }
    return render(request, 'ecommerceapp/checkout.html', context)

def contact(request):
    settings = Settings.objects.all().first()
    brands = Brands.objects.all()   
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    context ={'categories':categories,
               'sub_categories':sub_categories,
               'brands':brands,
               'settings': settings
               }
    return render(request, 'ecommerceapp/contact.html', context)

def news(request):
    settings = Settings.objects.all().first()   
    context ={
               'settings': settings,
               }
    return render(request, 'ecommerceapp/news.html', context)

def shop(request):
    settings = Settings.objects.all().first()
    brands = Brands.objects.all()
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    categoryID= request.GET.get('cat_id')

    if categoryID:
        products = Products.objects.filter(category=categoryID, is_active = True).order_by('-id')
    else:
        products = Products.objects.filter(is_active=True).order_by('-id')

    context ={'categories':categories,
               'sub_categories':sub_categories,
               'brands':brands,
               'products':products,
               'settings':settings,
               }
    return render(request, 'ecommerceapp/shop.html' ,context)

def single_news(request):
    settings = Settings.objects.all().first()
    brands = Brands.objects.all()   
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    context ={'categories':categories,
               'sub_categories':sub_categories,
               'brands':brands,
               'settings': settings
               }
    return render(request, 'ecommerceapp/single-news.html', context)

def single_product(request):
    settings = Settings.objects.all().first()
    brands = Brands.objects.all()   
    categories = Categories.objects.all()
    sub_categories = Sub_categories.objects.all()
    productID = request.GET.get('prod_id')
    if productID:
        products = Products.objects.filter(id=productID).first()

        if products:
            GetcategoryID = products.category.id
            related_prods = Products.objects.filter(category=GetcategoryID).all().order_by('-id')
    



    

    context={
        'products':products,
        'settings': settings,
        'brands':brands,
        'sub_categories':sub_categories,
        'categories':categories,
        'related_prods':related_prods
    }
    return render(request, 'ecommerceapp/single-product.html', context)