from django.db import models
from base.models import *
from user_profile.models import *
import datetime
# Create your models here.

class User_Payments(Base_Model):
    for_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "payments")
    for_order = models.ForeignKey(Orders, on_delete = models.CASCADE, related_name = "order")
    payment_id = models.CharField(max_length=36, blank=True, null=True)
    def gen_payment_id(self):
        order_id = str(self.for_order.u_id)[-6:]
        current_time = datetime.datetime.now()
        date_time_format = current_time.strftime("%S%M%H%y%m%d")
        payment_id = f"{order_id}{date_time_format}"
        return payment_id
    def save(self, *args, **kwargs):
        self.payment_id = self.gen_payment_id()
        super(User_Payments, self).save(*args, **kwargs)
    client_order_id = models.CharField(max_length = 1024, null = True, blank = True)
    client_payment_id = models.CharField(max_length = 1024 , null = True, blank = True)
    client_payment_signature = models.CharField(max_length = 1024, null = True, blank = True)
    
