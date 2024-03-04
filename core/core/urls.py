"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop.views import *
from products.views import *
from payments.views import *
from user_profile.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home,name="home"),
    path("shop",shop_all_products,name="shop_all_products"),
    path("<str:slug>",view_product,name="view_product"),
    path("category/<str:slug>",view_product_from_category,name="category"),
    path("user/registration",user_registration,name="user_registration"),
    path("user/login",user_login,name="user_login"),
    path("user/logout",user_logout,name="user_logout"),
    path("user/add-to-cart/<str:u_id>/<int:qty>",add_to_cart,name="add_to_cart"),
    path("user/remove-from-cart/<u_id>",remove_cart_items,name="remove_cart_items"),
    path("user/cart",user_cart,name="user_cart"),
    path("user/checkout/<cart_id>",check_out,name="check_out"),
    path("user/checkout/success/",payment_sucess,name="payment_sucess"),
    path("user/order",orders,name="user_order"),
    path("shop/contact",contact_page,name="contact_page")

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
