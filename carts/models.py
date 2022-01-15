from django.contrib.auth.models import AnonymousUser
from django.db import models
from category.models import Products
from accounts.models import Account

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class CartItems(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    cart = models.CharField(max_length=200,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.product_discount_price * self.quantity

class WishCart(models.Model):
    wishcart_id     = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)     

    def __str__(self):
        return self.cart_id   

class Wishlist(models.Model):
    wishcart        = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.product