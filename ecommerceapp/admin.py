from django.contrib import admin
from .models import Categories,Sub_categories,Products,Brands,UOMs,Settings,Deal,CartItem,Cart,Order

# Register your models here.
admin.site.register(Categories)
admin.site.register(Sub_categories)
admin.site.register(Products)
admin.site.register(Brands)
admin.site.register(UOMs)
admin.site.register(Settings)
admin.site.register(Deal)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)