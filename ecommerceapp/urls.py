from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.index, name="ecommerceapp-home" ),
    path('about/',views.about, name="ecommerceapp-about" ),
    path('404/',views.errorpage, name="ecommerceapp-404" ),
    path('cart/',views.cart, name="ecommerceapp-cart" ),
    path('checkout/',views.checkout, name="ecommerceapp-checkout" ),
    path('contact/',views.contact, name="ecommerceapp-contact" ),
    path('shop/',views.shop, name="ecommerceapp-shop" ),
    path('news/',views.news, name="ecommerceapp-news" ),
    path('single-news/',views.single_news, name="ecommerceapp-single-news" ),
    path('single-product/<int:id>/',views.single_product, name="ecommerceapp-single-product" ),
    path('shop/<int:category_id>/', views.shop_category, name="ecommerceapp-product-category" ),
    path('shop/search/', views.shop_search, name="ecommerceapp-product-search" )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
