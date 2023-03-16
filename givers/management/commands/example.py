from django.core.management.base import BaseCommand
from django.utils import timezone
from givers.models import Give,ShoppingCart
from datetime import datetime,timedelta, tzinfo
from django.db.models import Q


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        give=Give.objects.filter(gift_status='requested')
        a=timezone.now()
        current_time=a.replace(tzinfo=None)
        data = {
                'date_requested':None,
                'gift_recipient': '',
                'gift_status':'unpicked'}
        if give:
            for obj in give:
                w=obj.date_requested
                date_requested=w.replace(tzinfo=None)
                if current_time-timedelta(minutes=25)<=date_requested<=current_time+timedelta(minutes=25):
                    obj.date_requested= data['date_requested']
                    obj.gift_recipient= data['gift_recipient']
                    obj.gift_status=data['gift_status']
                    obj.save()

        time_lapse = timezone.now()-timedelta(minutes=25)
        ShoppingCart.objects.filter(status='in-cart',updated__range=[time_lapse,timezone.now()]).delete()