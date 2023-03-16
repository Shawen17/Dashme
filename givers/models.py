from django.db import models
from django import dispatch
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import pandas as pd
from Giveaway.settings import STATIC_ROOT
from django.utils import timezone
from django_resized import ResizedImageField
from .paystack import PayStack
import secrets
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
import random


def validate_number(value):
    if len(str(value))==10:
        return value
    else:
        raise ValidationError(_('Your phone number is incorrect'))



file_path = os.path.join(STATIC_ROOT,'givers/state.xlsx')
df = pd.read_excel(file_path)
df1= zip(df.value,df.representation)
states=[]
for i,j in df1:
    states.append((i,j))

file_path = os.path.join(STATIC_ROOT,'givers/vendor.xlsx')
df = pd.read_excel(file_path)
df1= zip(df.value,df.representation)
vendors=[]
for i,j in df1:
    vendors.append((i,j))

quantities=(

    ('single-items','single-items'),
    ('box','boxes/bags'),
    )

com_list=(
    ('enquiry','Enquiry'),
    ('complaint','Complaint'),
    ('report','Report'),
    ('others','Others')
)

gender =(
    ('male','Male'),
    ('female','Female'),
    ('O','Others')
)

categories =(
    ('furniture','Furniture'),
    ('clothes','Clothes'),
    ('shoes','Shoes'),
    ('toys','toys'),
    ('electronics','Electronics'),
    ('bag','Bags'),
    ('mobile','mobile-phones'),
    ('laptop','Laptops'),
    ('book','Books'),
    ('kitchen','Kitchen-utensils'),
    ('bicycle','Bicyle'),
    ('accessories','Accessories'),
    ('food','Food-stuffs'),
    ('groceries','Groceries'),
    ('generator','Generator'),
    ('beauty','Beauty-product'),
    ('natives','Natives'),
    ('corporate','Corporate')
)

status=(
    ('unpicked','unpicked'),
    ('requested','requested'),
    ('ordered','ordered')
)

product_level=(
    ('standard','standard'),
    ('premium','premium')
)


cart_choices=(
    ('in-cart','in-cart'),
    ('ordered','ordered')
)



class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    firstname = models.CharField(max_length=100,blank=True,default='')
    lastname = models.CharField(max_length=100,blank=True,default='')
    email =models.EmailField(max_length=150)
    state=models.CharField(max_length=50,choices=states)
    phone_number=models.BigIntegerField(default=int('08000000000'))
    sex=models.CharField(max_length=10,choices=gender,blank=True,default='')
    profile_pic = models.ImageField(upload_to='profiles',default='profiles/default_pic.jpg')
    bio = models.TextField(blank=True,default='')
    date_joined=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


@receiver(post_save,sender=User,dispatch_uid='user.created')
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Give(models.Model):

    state=models.CharField(max_length=40,choices=states)
    description=models.CharField(max_length=200)
    category=models.CharField(max_length=50,blank=True,default='',choices=categories)
    image= ResizedImageField()
    quantity=models.IntegerField()
    gender=models.CharField(max_length=10,choices=gender,blank=True,default='')
    tag_name=models.CharField(max_length=12,default='',blank=True,null=True)
    product_class=models.CharField(max_length=15,default='standard',choices=product_level)
    details=models.JSONField(default=dict,null=True)
    date_posted=models.DateTimeField(auto_now_add=True)
    date_requested = models.DateTimeField(null=True,blank=True)
    date_received = models.DateTimeField(null=True,blank=True)
    gift_recipient = models.CharField(max_length=100,default='',blank=True)
    gift_status = models.CharField(max_length=30,default='unpicked',blank=True,choices=status)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):

        while not self.tag_name:
            characters=list('0123456789')
            characters.extend('abcdefghijklmnopqrstuvwxyz')
            characters.extend('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            ticket=''
            for x in range(6):
                ticket +=random.choice(characters)
            tag_name=self.category[:3] + '_' + ticket
            object_with_similar_tag= Give.objects.filter(tag_name=tag_name)
            if not object_with_similar_tag:
                self.tag_name=tag_name

        super().save(*args, **kwargs)


class GiveImage(models.Model):
    give= models.ForeignKey(Give,default=None,on_delete=models.CASCADE,related_name='giveimage')
    images= models.ImageField(upload_to='givers/images/')

    def __str__(self):
        return self.giveimage.give


class ShoppingCart(models.Model):
    shopper=models.CharField(max_length=100)
    updated=models.DateTimeField(auto_now=True)
    product=models.ForeignKey(Give,on_delete=models.CASCADE,related_name='shopping_cart')
    status=models.CharField(max_length=20, default='in-cart',choices=cart_choices)

    def __str__(self):
        return str(self.product)


class ContactUs(models.Model):
    ticket=models.CharField(max_length=15,blank=True,default='')
    email= models.EmailField(max_length=150)
    subject= models.CharField(max_length=20,choices=com_list)
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.subject


class Received(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='person')
    gift_requested = models.OneToOneField(Give,on_delete=models.CASCADE,related_name='commodity')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_received = models.DateTimeField(auto_now_add=True)


# class Vendor(models.Model):
#     give = models.OneToOneField(Give,on_delete=models.CASCADE,related_name='gift')
#     ticket = models.CharField(max_length=10,blank=True,default='')
#     image=models.ImageField(upload_to='givers/images/')
#     state = models.CharField(max_length=50,choices=states,default='')
#     description=models.CharField(max_length=100)
#     request_date=models.DateTimeField(blank=True,null=True)
#     category = models.CharField(max_length=100,choices=categories)
#     giver_number=models.BigIntegerField(blank=True,null=True)
#     address=models.TextField(default='')
#     receiver_number=models.BigIntegerField(blank=True,null=True)
#     delivery_address =models.TextField(max_length=200,blank=True,null=True)
#     amount = models.IntegerField(blank=True,null=True)
#     payment_status = models.CharField(max_length=30,choices=pay_status,default='unpaid')
#     treated=models.BooleanField(default=False)

#     def __str__(self):
#         return self.give.description


# @receiver(post_save,sender=Give,dispatch_uid='give.created')
# def create_vendor_profile(sender,instance,created,**kwargs):
#     if created:
#         Vendor.objects.create(give=instance)
#     instance.gift.save()


class Transaction(models.Model):
    made_by = models.CharField( max_length=200,blank=True,null=True)
    made_on = models.DateTimeField(auto_now_add=True)
    items_id=models.JSONField(default=list,null=True)
    items=models.CharField(max_length=200,default='',blank=True)
    delivery_address=models.CharField(max_length=500,default='',null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    contact=models.CharField(max_length=15,default='',blank=True)
    ref = models.CharField( max_length=200,blank=True,null=True)
    email=models.EmailField(default='')
    verified=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)

    def __str__(self):
        return self.ref

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(16)
            object_with_similar_ref = Transaction.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref=ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack =PayStack()
        status,result = paystack.verify_payment(self.ref,self.amount)
        if status:
            self.verified =True
            self.save()
        if self.verified:
            return True
        return False

class Charge(models.Model):
    name= models.CharField(max_length=50)
    charge= models.IntegerField()


class Response(models.Model):
    email=models.EmailField(default='')
    comment=models.TextField()
    replied_on=models.DateTimeField(auto_now_add=True)
    replied_by=models.CharField(max_length=50)


class OnDeliveryTransaction(models.Model):
    made_by = models.CharField( max_length=50,blank=True,null=True)
    made_on = models.DateTimeField(auto_now_add=True)
    items_id=models.JSONField(default=list,null=True)
    items=models.CharField(max_length=200,default='',blank=True)
    amount = models.BigIntegerField()
    contact=contact=models.CharField(max_length=15,default='',blank=True)

    delivery_address=models.CharField(max_length=500,blank=True,null=True)
    ref = models.CharField( max_length=200,blank=True,null=True)
    email=models.EmailField(default='')
    delivered=models.BooleanField(default=False)
    settlement=models.BigIntegerField()

    def __str__(self):
        return self.ref

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(16)
            object_with_similar_ref = OnDeliveryTransaction.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref=ref
        super().save(*args, **kwargs)


class State(models.Model):
    name = models.CharField(max_length=25,default='lagos',choices=states)

    def __str__(self):
        return self.name



class DestinationCharge(models.Model):
    state=models.ForeignKey(State,on_delete=models.SET_NULL, null=True,default=1)
    city=models.CharField(max_length=100)
    charge=models.IntegerField()

    def __str__(self):
        return self.city


class Giveaway(models.Model):
    phone_number=models.IntegerField(validators=[validate_number])
    category=models.CharField(max_length=50,choices=categories)
    nature=models.CharField(max_length=50,blank=True,choices=quantities)
    quantity=models.IntegerField(blank=True,null=True)
    offered_on=models.DateField(auto_now_add=True)
    address=models.TextField()
    activate=models.BooleanField(default=False)
    received=models.BooleanField(default=False)

    def __str__(self):
        return self.category

class GiveawayCap(models.Model):
    name=models.CharField(max_length=50)
    number=models.IntegerField()

    def __str__(self):
        return self.name