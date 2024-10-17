from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string



def index(request): 
    feature_products = Products.objects.filter(is_feature =True, is_active =True).order_by('-created_at')
    trending_products = Products.objects.filter(is_trending =True, is_active =True).order_by('-created_at')
    deal = Deal.objects.filter(is_active=True).first()
    percentage = ((((deal.product.price-deal.product.discount_price))/(deal.product.price))*100).__round__(2)


    context ={
            "count": request.data["cart_count"],
            "categories": Categories.objects.all(),
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


    context ={
                "count": request.data["cart_count"],
                "categories": Categories.objects.all(),
                "settings": Settings.objects.first(),
                "brands": Brands.objects.all(),
                "title":"Error Page" 
               }
    return render(request, 'ecommerceapp/404.html', context)

def about(request):
    context ={"categories": Categories.objects.all(),
              "count": request.data["cart_count"],
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
                "title":"About Us"
               }
    return render(request, 'ecommerceapp/about.html', context)


def get_or_create_cart(request):
    session_key = request.session.session_key
    if request.user.is_authenticated:
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
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
                    "count": request.data["cart_count"],
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
    quantity = int(request.POST.get("quantity", 1))
    if product.stock_quantity >= quantity:
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, cost=product.cost_price, price=product.price,  total=quantity*product.price)

        if not created:
            cart_item.quantity += quantity
            cart_item.total = cart_item.quantity * cart_item.price
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        messages.add_message(request, messages.SUCCESS, "Product added to Cart")
    else:
        messages.add_message(request, messages.ERROR, f"Available quantity is {product.stock_quantity}")

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
                if cart_item.product.stock_quantity >= quantity:
                    cart_item.quantity = quantity
                    cart_item.total = cart_item.quantity * cart_item.price
                    cart_item.save()
                    messages.add_message(request, messages.SUCCESS, "Cart updated successfully...")
                else:
                    messages.add_message(request, messages.SUCCESS, f"{cart_item.product.stock_quantity} Qty of {cart_item.product.name} available")
                    break
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
            "count": request.data["cart_count"],
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
       cart_items =CartItem.objects.filter(cart_id=cart.id)
       cost = 0
       price = 0
       for item in cart_items:
           cost += item.cost*item.quantity
           price += item.price*item.quantity
        
       profit = price-cost
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       email = request.POST.get('email')
       phone = request.POST.get('phone')
       country = request.POST.get('country')
       city = request.POST.get('city')
       zip = request.POST.get('zip')
       address = request.POST.get('address')
       note = request.POST.get('note')
       payment = request.POST.get('payment')
       if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, cart_id=cart.id, first_name=first_name, last_name=last_name, email=email, phone=phone, country=country, city=city, zip=zip, address=address, note=note,payment=payment, cost=cost, price=price, profit=profit, total=request.data["total"])
       else:
           order = Order.objects.create(cart_id=cart.id, first_name=first_name, last_name=last_name, email=email, phone=phone, country=country, city=city, zip=zip, address=address, note=note,payment=payment, cost=cost, price=price, profit=profit, total=request.data["total"])
       

       for item in cart_items:
           OrderItems.objects.create(
               order = order,
               product = item.product,
               cost =item.cost,
               price = item.price,
               quantity = item.quantity,
               total = item.total,
           )
           product = get_object_or_404(Products, id = item.product.id)
           product.stock_quantity -= item.quantity
           product.save()

       order_items = OrderItems.objects.filter(order_id = order.id) 
       sub_total = 0
       for item in order_items:
        sub_total += item.total
       if sub_total >= 1500:
        shipping_charges = 0
       else:
        shipping_charges = 100
    
       grand_total = sub_total+shipping_charges    
       context={
           
            "sub_total":sub_total,
            "count": request.data["cart_count"],
            "shipping_charges":shipping_charges,
            "grand_total":grand_total,
           "order_items": order_items,
            "settings": Settings.objects.first(),
            "order":order,
            'recipient_name':first_name,
        }
       subject = 'Your Order Successfully Received'
       message = render_to_string('ecommerceapp/invoice.html', context)
       send_mail(subject,message,'order@hybridtech.org.pk',[email],html_message=message,
            )

       cart_items.delete()  
       if request.user.is_authenticated:
           pass
       else:      
        request.session.flush()
    
       
       messages.add_message(request, messages.SUCCESS, f"Your order has been placed! Order # {order.id}")
       return redirect('ecommerceapp-invoice', order_id=order.id)

def invoice_view(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItems.objects.filter(order_id = order.id)
    sub_total = 0
    for item in order_items:
        sub_total += item.total
    if sub_total >= 1500:
        shipping_charges = 0
    else:
        shipping_charges = 100
    
    grand_total = sub_total+shipping_charges

    context = {
                    "sub_total":sub_total,
                    "count": request.data["cart_count"],
                    "shipping_charges":shipping_charges,
                    "grand_total":grand_total,
                    "order":order,
                    "order_items": order_items,
                    "settings": Settings.objects.first(),
                    "count": request.data["cart_count"],
               }

    return render(request, 'ecommerceapp/invoice.html', context)
    
def tracking(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-id')
    else:
        orders = False
    context ={
            "orders":orders,
            "count": request.data["cart_count"],
            "categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
                "title":"tracking",
               }
    return render(request, 'ecommerceapp/tracking.html', context)
def order_track(request):
    query = request.GET.get('order_number')
    orders = Order.objects.filter(id=query)
    context ={
                "orders":orders,
                "count": request.data["cart_count"],
                "categories": Categories.objects.all(),
                "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
                "title":"tracking",
               }
    return render(request, 'ecommerceapp/tracking.html', context)

def contact(request):
    context ={"categories": Categories.objects.all(),
              "count": request.data["cart_count"],
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

    for product in products:
        if product.discount_price == 0:
            percentage = 0
        else:
            percentage = (((product.price-product.discount_price)/(product.price))*100).__round__(2)
        product.discount_per = percentage
        product.save()
        

    context ={"categories": Categories.objects.all(),
              "count": request.data["cart_count"],
            "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
               'products':products,
               "title":"Shop"
               }
    return render(request, 'ecommerceapp/shop.html' ,context)

def shop_category(request, category_id):
    products = Products.objects.filter(category_id=category_id, is_active=True)
    context ={"categories": Categories.objects.all(),
              "count": request.data["cart_count"],
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
              "count": request.data["cart_count"],
                "settings": Settings.objects.first(),
                "brands": Brands.objects.all(), 
               'products':products,
               "title":"Shop",
               }
    return render(request, 'ecommerceapp/shop.html' ,context)

def single_news(request):
    context ={"categories": Categories.objects.all(),
            "settings": Settings.objects.first(),
            "count": request.data["cart_count"],
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
        "count": request.data["cart_count"],
        "brands": Brands.objects.all(), 
        "products":products,
        'related_prods':related_prods,
        "title":"Product",
    }
    return render(request, 'ecommerceapp/single-product.html', context)