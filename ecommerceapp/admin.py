from django.contrib import admin
from .models import Categories,Sub_categories,Products,Brands,UOMs,Settings

# Register your models here.
admin.site.register(Categories)
admin.site.register(Sub_categories)
admin.site.register(Products)
admin.site.register(Brands)
admin.site.register(UOMs)
admin.site.register(Settings)