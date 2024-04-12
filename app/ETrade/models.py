from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Brand(models.Model):
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand_images', blank=True, null=True)

    def __str__(self):
        return self.brand


class Color(models.Model):
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.color


class UseType(models.Model):
    use_type = models.CharField(max_length=100)

    def __str__(self):
        return self.use_type


class ProcessorModel(models.Model):
    processor_model = models.CharField(max_length=100)

    def __str__(self):
        return self.processor_model


class DiskQuantity(models.Model):
    disk_quantity = models.CharField(max_length=100)

    def __str__(self):
        return self.disk_quantity


class RamSize(models.Model):
    ram_size = models.CharField(max_length=100)

    def __str__(self):
        return self.ram_size

class ProductType(models.Model):
    product_type = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.product_type

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='product_images', blank=True, null=True)
    price = models.FloatField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    use_type = models.ForeignKey(UseType, on_delete=models.CASCADE)
    processor_model = models.ForeignKey(
        ProcessorModel, on_delete=models.CASCADE)
    disk_quantity = models.ForeignKey(DiskQuantity, on_delete=models.CASCADE)
    ram_size = models.ForeignKey(RamSize, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True,default="")

    def __str__(self):
        return self.model
