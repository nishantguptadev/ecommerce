from django.contrib import admin
from django.utils.html import format_html

from django.urls import reverse
from .models import (
    Customer, Product, Cart, OrderPlaced, CustomerService
)

# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'titleshort', 'selling_price', 'discounted_price', 'brand', 'category','sub_category', 'product_image']
   

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_info', 'quantity']

    def product_info(self,obj):
        link = reverse("admin:ecomapp_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(OrderPlaced)
class OrderPlacesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','customer_info','product_info', 'quantity', 'ordered_date', 'status']
    
    def customer_info(self,obj):
        link = reverse("admin:ecomapp_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product_info(self,obj):
        link = reverse("admin:ecomapp_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(CustomerService)
class OrderPlacesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'query', 'detail']
