# Generated by Django 3.2.8 on 2022-04-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0011_ondeliverytransaction_settlement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='give',
            name='gift_status',
            field=models.CharField(blank=True, choices=[('unpicked', 'unpicked'), ('requested', 'requested'), ('received', 'received'), ('redeemed', 'redeemed'), ('paid', 'paid'), ('on-delivery', 'on-delivery')], default='unpicked', max_length=30),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='ticket',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
