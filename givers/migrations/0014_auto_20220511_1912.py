# Generated by Django 3.2.8 on 2022-05-11 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0013_alter_vendor_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='giver_contacted',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='receiver_contacted',
        ),
    ]
