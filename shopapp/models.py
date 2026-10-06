from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role_choice=(
        ('user','User'),
        ('seller','Seller'),
         ('admin','Admin')
         
    )
    
    status_choice=(
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    )
    role=models.CharField(max_length=10,choices=role_choice,default='user')
    
    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField( max_length=100)
    def __str__(self):
        return self.name
class Seller(models.Model):
    status_choice=(
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    )
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    shop_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pic=models.ImageField(upload_to='sellerpic/')
    status=models.CharField(max_length=15,choices=status_choice,default='pending')
    def __str__(self):
        return self.name
    
class Product(models.Model):
    seller=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='products/')
    seller_price=models.DecimalField(max_digits=10,decimal_places=2)
    mrp=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return self.name