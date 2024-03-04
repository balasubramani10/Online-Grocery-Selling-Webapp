from django.db import models
from base.models import *
from django.utils.text import slugify
# Create your models here.


#product category

class Product_Category(Base_Model):
    name = models.CharField(max_length = 128, unique=True, null = False, blank = False)
    slug = models.SlugField(unique=True, null = True, blank = True)
    image = models.ImageField(upload_to="Product_Category_Images", null = True, blank = True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(Product_Category,self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    
#product Manufacturer
    
class Product_Manufacturer(Base_Model):
    name  = models.CharField(max_length = 128,unique = True, null = False, blank = False)
    def __str__(self):
        return self.name
    
#product Brand
    
class Product_Brand(Base_Model):
    manufacturer = models.ForeignKey(Product_Manufacturer, on_delete = models.CASCADE, related_name = "brand")
    name  = models.CharField(max_length = 128,unique = True , null = False, blank = False)
    def __str__(self):
        return self.name

class Product(Base_Model):
    category = models.ForeignKey(Product_Category, on_delete = models.CASCADE, related_name = "product")
    manufacturer = models.ForeignKey(Product_Manufacturer, on_delete = models.CASCADE, related_name = "product")
    brand = models.ForeignKey(Product_Brand, on_delete = models.CASCADE, related_name = "product")
    name  = models.CharField(max_length = 128, null = False, blank = False)
    description = models.TextField(max_length = 1024, null = False, blank = False)
    retail_price = models.FloatField(null = False, blank = False)
    selling_price = models.FloatField(null = False, blank = False)
    stock = models.IntegerField(default = 0)
    slug = models.SlugField(unique=True, null = True, blank = True)
    def discount_percentage(self):
        return round(((self.retail_price - self.selling_price)/self.retail_price)*100)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Product_Images(Base_Model):
    for_product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "images")
    image = models.ImageField(upload_to="Product_Images")
    def __str__(self):
        return self.for_product.name
     





