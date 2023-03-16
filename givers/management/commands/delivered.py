from django.core.management.base import BaseCommand
from django.utils import timezone
from givers.models import Transaction,OnDeliveryTransaction



class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        trans=Transaction.objects.filter(delivered=False,verified=True)
        on_delivery=OnDeliveryTransaction.objects.filter(delivered=False)

        if trans:
            for obj in trans:
                b=timezone.now()-obj.made_on
                diff=int(b.days)
                if diff>=8:
                    obj.delivered=True
                    obj.save()
        if on_delivery:
            for obj in on_delivery:
                b=timezone.now()-obj.made_on
                diff=int(b.days)
                if diff>=8:
                    obj.delivered=True
                    obj.save()
        self.stdout.write("It's now done")