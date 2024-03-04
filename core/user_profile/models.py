from django.db import models
from base.models import *
import datetime
from django.contrib.auth.models import User
from products.models import *

# Create your models here.

class User_Profile(Base_Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "profile",  null=True)
    def cart_items_count(self):
        count = Shopping_Cart_Items.objects.filter(for_cart__for_user = self.user, for_cart__payment_status = False).count()
        return count
class User_Shopping_Cart(Base_Model):
    for_user= models.ForeignKey(User, on_delete = models.CASCADE, related_name = "cart")
    payment_status = models.BooleanField(default = False)
    def cart_total_retail_price(self):
        cart_items = self.cart_items.all()
        total = []
        for i in cart_items:
            total.append(i.subtotal_retail_price())
        return sum(total)
    def cart_total(self):
        cart_items = self.cart_items.all()
        total = []
        for i in cart_items:
            total.append(i.subtotal())
        return sum(total)
    def cart_dicount(self):
        cart_items = self.cart_items.all()
        total = []
        for i in cart_items:
            total.append((i.product.retail_price)*(i.product_qty))
        total_price = sum(total)
        discount = total_price - self.cart_total()
        return discount
    
    def __str__(self):
        return self.for_user.username
class Shopping_Cart_Items(Base_Model):
    for_cart = models.ForeignKey(User_Shopping_Cart, on_delete = models.CASCADE, related_name = "cart_items")
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "in_cart_product")
    product_qty = models.IntegerField(null = False, blank = False)
    def subtotal_retail_price(self):
        subtotal = (self.product.retail_price) * (self.product_qty)
        return subtotal
    def subtotal(self):
        subtotal = (self.product.selling_price) * (self.product_qty)
        return subtotal
    def __str__(self):
        return self.product.name   
class Orders(Base_Model):
    for_user = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "orders", editable=False)
    for_cart = models.ForeignKey(User_Shopping_Cart, on_delete = models.PROTECT, related_name = "orders_cart", editable=False)
    items = models.ManyToManyField(Shopping_Cart_Items , related_name="orders_items" )
    order_id = models.CharField(max_length=64, blank=True, null=True, )
    def gen_order_id(self):
        user_id =  str(self.for_user.profile.u_id)[0:3] + str(self.for_user.id)[:-3]
        current_time = datetime.datetime.now()
        date_time_format = current_time.strftime("%S%M%H%y%m%d")
        order_id = f"{user_id}{date_time_format}"
        return (order_id)
    time = models.DateTimeField(auto_now_add = True, )
    payment_status = models.BooleanField(default = False)
    def save(self, *args, **kwargs):
        self.order_id = self.gen_order_id()
        super(Orders, self).save(*args, **kwargs)
    def order_total(self):
        total = self.for_cart.cart_total()
        return total
    def __str__(self):
        return self.order_id
