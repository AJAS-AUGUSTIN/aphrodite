from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import UUIDField
from accounts.models import Account
from category.models import Products

# Create your models here.

class Order(models.Model):
    order_id            = models.CharField(max_length = 50, blank = True)
    payment_method      = models.CharField(max_length = 50, blank = True)
    user                = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    delivered_address   = models.CharField(max_length=200, blank= True)
    delivery_status     = models.CharField(max_length = 50, blank = True)        

class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    # payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    products_id = models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    anonymous_user = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    sub_total = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grand_total = models.IntegerField(null=True)

    def __str__(self):
        return self.product.product_name

#class Order(models.Model):
#     STATUS = (
#         ('New','New'),
#         ('Accepted','Accepted'),
#         ('Completed','Completed'),
#         ('Cancelled','Cancelled'),
#     )
#     order_id = models.CharField(max_length=50,blank=True)
#     user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
#     user_address = models.CharField(max_length=2500,null=True)
#     payment_mode = models.CharField(max_length=100,null=True)
#     order_number = models.CharField(max_length=20)
#     grand_total = models.FloatField(null=True)
#     tax = models.FloatField()
#     status = models.CharField(max_length=10,choices=STATUS,default='New')
#     is_orderd = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
      
#     def __str__(self):
#         return self.first_name
        
# class Payment(models.Model):
#     user = models.ForeignKey(Account,on_delete=models.CASCADE)
#     payment_id = models.CharField(max_length=100)
#     payment_method = models.CharField(max_length=100)
#     amount_paid = models.CharField(max_length=100)
#     status = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.payment_id


