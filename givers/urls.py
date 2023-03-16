from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("transaction/",views.initiate_payment,name="initiate-payment"),
    path('<str:ref>/',views.verify_payment,name="verify-payment"),
]
