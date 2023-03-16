from datetime import datetime,timedelta, tzinfo
from django.utils import timezone
from django.db.models import Q
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Giveaway.settings')
import django
django.setup()
from models import Give,Vendor


vend=Vendor.objects.filter(payment_status='unpaid')
give=Give.objects.filter(~Q(gift_status='received') & Q(date_requested__isnull=False))
data = {
        'date_requested':None,
        'gift_recipient': '',
        'gift_status':'unpicked'}
for obj in give:
    b=timezone.now()-obj.date_requested
    diff=int(b.days)
    if diff>=2 and obj.gift.payment_status=='unpaid':
        obj.date_requested= data['date_requested']
        obj.gift_recipient= data['gift_recipient']
        obj.gift_status=data['gift_status']
        obj.gift.ticket=''
        obj.gift.amount=None
        obj.gift.receiver_number=None
        obj.gift.delivery_address=None
        obj.gift.giver_contacted=False
        obj.gift.receiver_contacted=False
        obj.save()
