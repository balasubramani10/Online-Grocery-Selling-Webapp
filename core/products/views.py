from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.contrib import messages
# Create your views here.


def shop_all_products(request):

    
    if request.GET.get("header_search"):
        user_input = request.GET.get("header_search")
        products = Product.objects.filter(name__icontains = user_input)
        context = {
            "products" : products
        }
    else:
        products = Product.objects.all()
    context = {
        "products" : products
    }
    return render(request,"products/allProducts.html",context)
   

def view_product_from_category(request, slug):
  
        
    products = Product.objects.filter(category__slug = slug)
    context = {
        "products" : products
    }
    return render (request,"products/allProducts.html",context)

   

def view_product(request,slug):
    product = Product.objects.filter(slug = slug)
    context = {
            "product" : product
            }
    return render(request,"products/viewProduct.html",context)