from django.shortcuts import render
from products.models import *
# Create your views here.

def home(request):
    all_category = Product_Category.objects.all().order_by("created_at")
    today_offer = Product.objects.all()[:8]
    top_sellings = Product.objects.all()[:10]


    context = {
        "all_category" : all_category,
        "today_offer_mini" : today_offer[:8],
        "top_sellings_mini" : top_sellings[5:]
    }
    
    return render (request, "shop/home.html",context)

def contact_page(request):
    return render(request,"components/contact.html")

        

