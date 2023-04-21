from django.core.management.base import BaseCommand
from django.utils import timezone
from givers.models import Give,ShoppingCart
from datetime import timedelta



class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        a=timezone.now()

        Give.objects.filter(date_requested__lte=a+timedelta(minutes=20),gift_status='requested').update(date_requested=None,gift_recipient='',gift_status='unpicked')

        ShoppingCart.objects.filter(status='in-cart',updated__lte=a+timedelta(minutes=20)).delete()