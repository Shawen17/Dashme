from functools import partial
from itertools import groupby
from operator import attrgetter
from .models import OnDeliveryTransaction,Transaction,Give,Charge
from django.forms.models import ModelChoiceIterator, ModelChoiceField
from django.utils import timezone

class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in groupby(queryset, self.groupby):
            yield (group, [self.choice(obj) for obj in objs])


class GroupedModelChoiceField(ModelChoiceField):
    def __init__(self, *args, choices_groupby, **kwargs):
        if isinstance(choices_groupby, str):
            choices_groupby = attrgetter(choices_groupby)
        elif not callable(choices_groupby):
            raise TypeError('choices_groupby must either be a str or a callable accepting a single argument')
        self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)






def final_checkout(Model,account_owner,cost,delivery_address,contact):

    service_charge=Charge.objects.get(name='standard').charge
    #change gift_recipient=user.email
    give=Give.objects.filter(gift_recipient=account_owner.profile.email,gift_status='requested')
    ondelivery_total=cost+service_charge
    if ondelivery_total>=2500:
        paystack_charge=100 + (0.015*ondelivery_total)
    else:
        paystack_charge=(0.015*ondelivery_total)

    paystack_charge=round(paystack_charge,2)
    paid_delivery_total=cost+service_charge+paystack_charge
    ids=[i.id for i in give]
    item=[i.description + '_' + i.tag_name for i in give]
    item=', '.join(item)
    vat=0.075*service_charge

    if isinstance(Model,Transaction):
        data={
        'made_by':account_owner,
        'email':account_owner.email,
        'items_id':ids,
        'items':item,
        'amount':paid_delivery_total,
        'delivery_address':delivery_address,
        'contact': str(contact)
        }
        return data,paystack_charge,service_charge
    elif isinstance(Model,OnDeliveryTransaction):

        data={
        'made_by':account_owner,
        'email':account_owner.email,
        'made_on':timezone.now(),
        'items':item,
        'settlement':service_charge+500,
        'items_id':ids,
        'contact':str(contact),
        'amount':ondelivery_total+vat,
        'delivery_address':delivery_address,
        }
        return data,service_charge




