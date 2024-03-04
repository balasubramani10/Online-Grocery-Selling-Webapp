from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from user_profile.models import *
from products.models import *
from .models import *
import razorpay
# Create your views here.

def payment_sucess(request):
    if request.user.is_authenticated:
        client_order_id = request.GET.get("razorpay_order_id")
        client_payment_id = request.GET.get("razorpay_payment_id")
        client_payment_signature = request.GET.get("razorpay_signature")
        order_id = request.GET.get("user_order_id")
        order = Orders.objects.get(u_id = order_id)
        user = request.user
        cart = User_Shopping_Cart.objects.get(for_user = user)
        new_payment = User_Payments.objects.create(
            for_user = user,
            for_order = order,
            client_order_id = client_order_id,
            client_payment_id = client_payment_id,
            client_payment_signature = client_payment_signature,
        )
        new_payment.save()
        order.payment_status = True
        cart.payment_status = True
        order.for_cart.payment_status = True
        order.save()
        
        
        cart_items = cart.cart_items.all()
        cart_items.delete()
        context = {
            "new_payment" : new_payment
        }
        
        
        return render(request, "payments/sucess.html")
        
        
