from django.contrib import admin
from .models import *
# Register your models here.


class User_Cart_Items(admin.StackedInline):
    model = Shopping_Cart_Items

class User_Shoping_Cart(admin.ModelAdmin):
    inlines = [User_Cart_Items]

class User_Profile_Admin(admin.ModelAdmin):
    list_display = ["cart_items_count"]

class User_Order_Admin(admin.ModelAdmin):
    list_display = ["for_user", "order_id" , "payment_status"]

admin.site.register(User_Shopping_Cart , User_Shoping_Cart)
admin.site.register(Shopping_Cart_Items)
admin.site.register(Orders, User_Order_Admin)
admin.site.register(User_Profile, User_Profile_Admin)
