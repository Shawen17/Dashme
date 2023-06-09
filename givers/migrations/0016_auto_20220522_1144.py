# Generated by Django 3.2.8 on 2022-05-22 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0015_destinationcharge_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ondeliverytransaction',
            old_name='verified',
            new_name='delivered',
        ),
        migrations.RenameField(
            model_name='vendor',
            old_name='delivered',
            new_name='treated',
        ),
        migrations.AddField(
            model_name='ondeliverytransaction',
            name='items_id',
            field=models.JSONField(default=list, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='delivery_address',
            field=models.CharField(default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='items_id',
            field=models.JSONField(default=list, null=True),
        ),
    ]
