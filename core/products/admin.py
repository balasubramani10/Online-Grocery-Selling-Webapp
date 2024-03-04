from django.contrib import admin
from .models import *
# Register your models here.

class Product_Images(admin.StackedInline):
    model = Product_Images

class Product_Admin(admin.ModelAdmin):
    inlines = [Product_Images]
    list_display = ["name" , "category", "retail_price", "selling_price", "stock" , "discount_percentage"]
    
admin.site.register(Product, Product_Admin)
admin.site.register(Product_Category)
admin.site.register(Product_Manufacturer)
admin.site.register(Product_Brand)

