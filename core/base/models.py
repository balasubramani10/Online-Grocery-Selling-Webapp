from django.db import models
import uuid
# Create your models here.

class Base_Model(models.Model):
    u_id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        abstract = True