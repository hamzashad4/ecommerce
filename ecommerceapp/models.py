from django.db import models
from datetime import datetime
from django.conf import settings


class Categories(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Sub_categories(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Brands(models.Model):
    brand_image = models.ImageField(upload_to='ecommerceapp/BrandImages/',null=True, blank=True)
    brand_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name

class UOMs(models.Model):
    UOM = models.CharField(max_length=255)
    
    def __str__(self):
        return self.UOM

class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    UOM = models.ForeignKey('UOMs', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brands', on_delete=models.SET_NULL, null=True, related_name ='brand')
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name ="products")
    price =models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ecommerceapp/ProductImages/', null=True, blank=True)
    is_active =models.BooleanField(default=True)
    is_feature = models.BooleanField(default=True)
    is_trending = models.BooleanField(default=True)
    created_at =models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
class Settings(models.Model):
    favicon = models.ImageField(upload_to='ecommerceapp/settingImages/', null=True, blank=True)
    logo = models.ImageField(upload_to='ecommerceapp/settingImages/', null=True, blank=True)
    site_title = models.CharField(max_length=255)
    Sologun = models.CharField(max_length=255)
    banner = models.ImageField(upload_to="ecommerceapp/settingImages/", null=True, blank=True)
    free_shipping = models.DecimalField(max_digits=10, decimal_places=2)
    return_days = models.PositiveIntegerField()
    copyright_year = models.CharField(max_length=255)
    copyright_name = models.CharField(max_length=255)
    distributor_by = models.CharField(max_length=255)
    facebook_url = models.URLField(max_length=500)
    twitter_url = models.URLField(max_length=500)
    instagram_url = models.URLField(max_length=500)
    linkedin_url = models.URLField(max_length=500)
    address = models.TextField()
    email = models.EmailField(max_length=500)
    phone_number = models.CharField(max_length=255)
    location_url = models.URLField(max_length=1000)

    def __str__(self):
        return self.site_title
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart #{self.id}, {self.session_key}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} in Cart #{self.cart.id}"
    
    def get_total_price(self):
        return self.quantity * self.product.price