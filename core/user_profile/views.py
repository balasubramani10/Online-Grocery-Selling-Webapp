from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from products.models import *
from user_profile.models import *
from payments.models import *
import razorpay
# Create your views here.



def user_registration(request):
    try:
        if request.method == "POST":
            user_input = request.POST
            user_first_name = user_input.get("user_profile_name")
            user_last_name = user_input.get("user_profile_last_name")
            user_email = user_input.get("user_email")
            user_password = user_input.get("user_set_password")
            user_confirm_password = user_input.get("user_set_password_confirm")
            existing_user = User.objects.filter(username = user_email)
            if user_first_name == ""  or user_email == "" or user_password == "" or user_confirm_password == "":
                messages.error(request,"Fields With * Needs To Be Filled")
                return HttpResponseRedirect(request.path_info)
            elif existing_user.exists():
                messages.error(request,"User With Same Email Already Exists")
                return HttpResponseRedirect(request.path_info)
            elif user_password != user_confirm_password:
                messages.error(request,"Both The Password hould Be Same")
                return HttpResponseRedirect(request.path_info)
            else:
                new_user = User.objects.create(
                    username = user_email,
                    first_name = user_first_name,
                    email = user_email
                    )
                if user_last_name != "":
                    new_user.last_name = user_last_name
                new_user.set_password( user_password)
                new_user.save()
                new_user_profile = User_Profile.objects.create(
                    user = new_user
                )
                new_user = authenticate(username = user_email,password =  user_password)
                login(request, new_user)
                return redirect("/")
                
        return render(request,"user-profile/userReg.html")
    except Exception as e:
        print(e)
    pass

def user_login(request):
    try:
        if request.user.is_authenticated:
            return redirect("/")
        else:
            if request.method == "POST":
                user_input = request.POST
                user_email = user_input.get("user_email")
                user_password = user_input.get("user_password")
                existing_user = User.objects.filter(username = user_email)
                current_user = authenticate(username = user_email,password =  user_password)
                if user_email == "" or user_password == "":
                    messages.error(request,"Fields With * Needs To Be Filled")
                    return HttpResponseRedirect (request.path_info)
                elif not existing_user.exists():
                    messages.error(request,"You Don't Have A Account With Us, Kindly Create Before Login")
                    return HttpResponseRedirect (request.path_info)
                elif not current_user:
                    messages.error(request,"Incorrect Password")
                else:
                    login(request, current_user)
                    return redirect("/")
        return render(request,"user-profile/userLogin.html")
    except Exception as e:
        print(e)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")

def add_to_cart(request,u_id,qty):
    if request.user.is_authenticated:
        product = Product.objects.get(u_id = u_id)
        user = request.user
        obj = Shopping_Cart_Items.objects.filter(for_cart__for_user = user , product = product)
        if product.stock >= 1:
            if obj.exists():
                obj.update(product_qty= qty)
                return redirect("/user/cart")
            else:
                cart , _ = User_Shopping_Cart.objects.get_or_create(
                    for_user = user,
                    payment_status = False
                )
                shopping_Cart_Items = Shopping_Cart_Items.objects.create(
                    for_cart = cart,
                    product = product,
                    product_qty = qty
                )
                shopping_Cart_Items.save()
                return redirect("/user/cart")
        else:
            return redirect("/")
    else:
        return render(request, "user-profile/userLogin.html", )

def remove_from_cart(request):
    return redirect("/")

def user_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = User_Shopping_Cart.objects.filter(for_user = user)
        if cart.exists():

            cart_items = Shopping_Cart_Items.objects.filter(for_cart = cart[0])
            context = {
                "cart" : cart,
                "cart_items" : cart_items
            }
        
        
            print("cart",cart[0].cart_dicount())
            return render(request,"user-profile/userCart.html",context)
    else:
        return render(request, "user-profile/userLogin.html", )

            

def remove_cart_items(request,u_id):
    if request.user.is_authenticated:
        cart_item = Shopping_Cart_Items.objects.filter(u_id = u_id)
        cart_item.delete()
        return redirect("/user/cart")
    else:
        return render(request, "user-profile/userLogin.html", )


def check_out(request, cart_id):
    if request.user.is_authenticated:
        cart = User_Shopping_Cart.objects.get(u_id = cart_id)
        cart_items = Shopping_Cart_Items.objects.filter(for_cart = cart)
        order = Orders.objects.create(
            for_user = request.user,
            for_cart = cart,
            
            )
        order.items.set(cart_items)
       
        
       
        order.save()
        print(order.order_total())
        
        user = request.user
        client = razorpay.Client(auth = ("testKey","testid"))
        order = Orders.objects.filter(for_user = user)
        order = order[0]
        payment = client.order.create(
            {
                "amount" : order.for_cart.cart_total()*100,
                "currency" : "INR",
                "payment_capture" : 1,
            }
            )
        
        payment_details = User_Payments.objects.create(
            for_user = user,
            for_order = order,
            client_order_id = payment["id"],

        )
        payment_details.save()
        context = {
            "payment" : payment,
            "order" : order,
            "payment_details" :payment_details
        }
        
        return render(request, "payments/checkout.html",context)
    else:
        return render(request, "user-profile/userLogin.html", )

def orders(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Orders.objects.filter(for_user = user)
        context = {
            "orders" : orders
        }
        return render(request, "user-profile/userOrder.html", context)
    else:
        return render(request, "user-profile/userLogin.html", )

    

