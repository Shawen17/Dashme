from django.db import models
from django.forms.models import ALL_FIELDS
from .models import Give,Profile,ContactUs,states,Response,Giveaway,Transaction
from django.forms import ModelForm, fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class ContactUsForm(ModelForm):

    class Meta:
        model= ContactUs
        fields = ('email','subject','ticket','body')


class GiveForm(ModelForm):

    class Meta:
        model= Give
        fields = ('description','category','image','quantity')

class SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Again'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    firstname = forms.CharField(max_length= 100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    lastname = forms.CharField(max_length= 100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    username = forms.CharField(max_length= 200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    phone_number=forms.IntegerField(required=True)
    state=forms.ChoiceField(choices=states)
    class Meta:
        model = User
        fields = ('firstname','lastname','username','email','phone_number','state','password1','password2')

class Profileform(ModelForm):

    firstname = forms.CharField(max_length= 100)
    lastname = forms.CharField(max_length= 100)
    email = forms.EmailField(max_length=100)
    phone_number=forms.IntegerField(required=True)
    class Meta:
        model = Profile
        fields = ('profile_pic','firstname','lastname','email','sex','state','phone_number')

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields=('contact','delivery_address')


class SendEmailForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model=Response
        fields=('comment',)




class GiveawayForm(ModelForm):
    #address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Full Address'}))

    class Meta:
        model= Giveaway
        fields=('phone_number','category','nature','quantity','address')