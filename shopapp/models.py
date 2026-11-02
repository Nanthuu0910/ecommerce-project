from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


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
    status = models.CharField(max_length=10,choices=status_choice,default='approved')

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField( max_length=100)
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='subcategories')
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
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='products/')
    stock=models.PositiveIntegerField(default=0)
   
    def delete(self,*args,**kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args,*kwargs)
    
    def __str__(self):
        return self.name
class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(null=False,blank=False)
    order_id=models.CharField(max_length=15)
    total=models.IntegerField(null=False,blank=False)

    def save(self,*args,**kwargs):

        self.total=self.product.price*self.quantity
        self.order_id=f"ord-{uuid.uuid4()}"
        super().save(*args,**kwargs)
class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    
    time=models.DateTimeField()
    status_info=(
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('shipped','Shipped'),
        ('cancelled','Cancelled'),
        ('delivered','Delivered')
    )
    status=models.CharField(max_length=15,choices=status_info,default='pending')
    payment_status=(
        ('unpaid','Unpaid'),
        ('paid','Paid')
        
    )
    payment=models.BooleanField(choices=status_info,default='False')

    def __str__(self):
        return self.user.username

