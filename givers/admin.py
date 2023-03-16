from django.contrib import admin
from .models import Profile,Give,GiveImage,ContactUs,Received,Transaction,Charge,Response,OnDeliveryTransaction,State,DestinationCharge,Giveaway,ShoppingCart,GiveawayCap
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse
from .forms import SendEmailForm
from django.shortcuts import render
from django.utils import timezone





@admin.register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display=('shopper','product','updated','status')


@admin.register(Response)
class ResponseAdmin(ModelAdmin):
    list_display=('email','comment','replied_on','replied_by')
    ordering=('-replied_on',)
    search_fields=('email',)


@admin.register(State)
class StateAdmin(ModelAdmin):
    list_display=('name',)


@admin.register(GiveawayCap)
class GiveawayCapAdmin(ModelAdmin):
    list_display=('name','number')


@admin.register(DestinationCharge)
class DestinationChargeAdmin(ModelAdmin):
    list_display=('state','city','charge')
    actions=['export_rate']

    def export_rate(self,request,queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['Destination','Charge'])
        orders = queryset.values_list('city','charge')
        for order in orders:
            writer.writerow(order)
        return response
    export_rate.short_description = 'Export to csv'


@admin.register(Charge)
class ChargeAdmin(ModelAdmin):
    list_display=('name','charge')

@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display=('ref','email','made_by','made_on','items_id','items','delivery_address','contact','amount','verified','delivered')
    ordering =('-made_on',)
    search_fields =('ref','email')
    actions=['mark_delivered']

    def mark_delivered(self,request,queryset):
        queryset.update(delivered=True)
        for i in queryset:
            gives=Give.objects.filter(id__in=i.items_id).update(gift_status='received',date_received=timezone.now())

    mark_delivered.short_description = 'Mark as Delivered'



@admin.register(OnDeliveryTransaction)
class OnDeliveryTransactionAdmin(ModelAdmin):
    list_display=('ref','email','made_by','made_on','items_id','items','delivery_address','contact','amount','settlement','delivered',)
    ordering =('-made_on',)
    search_fields =('ref','email')
    actions=['mark_delivered','export_orders']

    def mark_delivered(self,request,queryset):
        queryset.update(delivered=True)
        for i in queryset:
            gives=Give.objects.filter(id__in=i.items_id).update(gift_status='received',date_received=timezone.now())

    def export_orders(self,request,queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['Ref','Made By','Order Date','Pickup Location','Delivery Address','Amount','Settlement','Payment Status'])
        orders = queryset.values_list('ref','made_by','made_on','pickup_location','delivery_address','amount','settlement','verified')
        for order in orders:
            writer.writerow(order)
        return response

    mark_delivered.short_description = 'Mark as Delivered'
    export_orders.short_description = 'Export to csv'



@admin.register(Received)
class ReceivedAdmin(ModelAdmin):
    list_display =('gift_requested','date_requested','date_received')
    ordering = ('-date_requested','-date_received')
    search_fields = ('gift_requested',)

@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    list_display =('ticket','email','subject','body','date','status')
    ordering =('subject','status',)
    search_fields = ('email','ticket')
    actions=['send_email']


    def send_email(self, request, queryset):
        selected=[]
        queryset.update(status=True)
        for i in queryset:

            selected.append(i.email)
        request.session['selected'] = selected
        form = SendEmailForm(initial={'users': queryset})
        return render(request, 'givers/send_email.html', {'form': form})

    send_email.short_description = "Reply Message"



@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display=('firstname','lastname','email','state','phone_number','sex','profile_pic','date_joined')
    search_fields=('state','date_joined','email')
    ordering = ('-date_joined',)
    actions=['send_email']

    def send_email(self, request, queryset):
        selected=[]
        for i in queryset:
            if i.email:
                selected.append(i.email)
        request.session['selected'] = selected
        form = SendEmailForm(initial={'users': queryset})
        return render(request, 'givers/broadcast_email.html', {'form': form})

    send_email.short_description = "Send Message"

class ProfileInline(admin.StackedInline):
    model=Profile
    fk_name = 'user'
    can_delete = False
    verbose_name_plural = 'profile'



class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


class GiveImageInline(admin.StackedInline):
    model=GiveImage
    fk_name= 'give'
    can_delete= False
    verbose_name_plural = 'giveimage'

# class VendorInline(admin.StackedInline):
#     model= Vendor
#     fk_name= 'give'
#     can_delete = False
#     verbose_name_plural= 'gift'

@admin.register(Give)
class GiveAdmin(ModelAdmin):
    # inlines=(GiveImageInline,VendorInline)
    inlines=(GiveImageInline,)
    list_display= ('description','category','gift_recipient','state','tag_name','gender','image','quantity','product_class','details','date_posted','date_requested','date_received','gift_status')
    search_fields=('category','description','tag_name','gift_recipient')
    ordering=('-date_posted','category','-date_requested','tag_name')
    actions = ['send_mail']


    def send_mail(self, request, queryset):
        selected=[]
        for i in queryset:
            if i.gift_recipient:
                selected.append(i.gift_recipient)
        request.session['selected'] = selected
        form = SendEmailForm(initial={'users': queryset})
        return render(request, 'givers/broadcast_email.html', {'form': form})

    send_mail.short_description = "Send Email"





@admin.register(GiveImage)
class GiveImageAdmin(ModelAdmin):
    pass


# @admin.register(Vendor)
# class VendorAdmin(ModelAdmin):
#     list_display=('ticket','give','description','image','category','request_date','receiver_number','delivery_address','amount','payment_status','treated')
#     ordering=('-request_date','treated')
#     search_fields=('ticket','description')
#     actions=['mark_treated','export_orders','mark_return']


#     def mark_treated(self,request,queryset):
#         queryset.update(treated=True)

#     def mark_return(self,request,queryset):
#         queryset.update(payment_status='unpaid',amount=None,delivery_address=None,receiver_number=None,request_date=None,ticket='')
#         data = {
#                 'date_requested':None,
#                 'gift_recipient': '',
#                 'gift_status':'unpicked'}
#         for i in queryset:
#             give=Give.objects.get(description=i.description)
#             give.date_requested=data['date_requested']
#             give.date_received=data['date_requested']
#             give.gift_recipient=data['gift_recipient']
#             give.gift_status=data['gift_status']
#             give.save(update_fields=['date_requested','gift_recipient','gift_status','date_received'])
#             vend= Vendor.objects.get(give=give)
#             vend.payment_status='unpaid'
#             vend.save(update_fields=['payment_status'])

#     def export_orders(self,request,queryset):
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="orders.csv"'
#         writer = csv.writer(response)
#         writer.writerow(['Ticket','State','Description','Category','Pickup Contact','Pickup Address','Receiver Contact',
#         'Delivery Address','Amount','Payment Status','Treated'])
#         orders = queryset.values_list('ticket','state','description','category','giver_number','address',
#         'receiver_number','delivery_address','amount','payment_status','treated')
#         for order in orders:
#             writer.writerow(order)
#         return response

#     mark_return.short_description='Return Item(s)'
#     export_orders.short_description = 'Export to csv'
#     mark_treated.short_description = 'Mark as Treated'


@admin.register(Giveaway)
class GiveawayAdmin(ModelAdmin):
    list_display=('phone_number','category','offered_on','nature','quantity','address','activate','received')
    actions=['mark_activated','mark_received']

    def mark_activated(self,request,queryset):
        queryset.update(activate=True)

    def mark_received(self,request,queryset):
        queryset.update(received=True)

    mark_received.short_description='Mark as Received'
    mark_activated.short_description = 'Mark as Active'


admin.site.unregister(User)
admin.site.register(User,UserAdmin)

