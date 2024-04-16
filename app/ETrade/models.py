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
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    use_type = models.ForeignKey(UseType, on_delete=models.CASCADE,blank=True,null=True)
    processor_model = models.ForeignKey(
        ProcessorModel, on_delete=models.CASCADE,blank=True,null=True)
    disk_quantity = models.ForeignKey(DiskQuantity, on_delete=models.CASCADE,blank=True,null=True)
    ram_size = models.ForeignKey(RamSize, on_delete=models.CASCADE,blank=True,null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True,default="")

    def __str__(self):
        return self.model


class BasketProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.model
    
    class Meta:
        verbose_name_plural = 'Products in Basket'
        unique_together = ('user', 'product')
        

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Profiles'


class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=150,null=True,blank=True)
    province = models.CharField(max_length=150,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    neighborhood = models.CharField(max_length=100,null=True,blank=True)
    postal_code = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        verbose_name_plural = 'Adresses'
        
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Favorites'
        
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    comment = models.TextField(max_length=500)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Comments'
        