# Generated by Django 3.2.8 on 2021-11-19 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0003_alter_give_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='checksum',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='order_id',
        ),
        migrations.AddField(
            model_name='transaction',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='transaction',
            name='ref',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='give',
            name='gift_status',
            field=models.CharField(blank=True, choices=[('unpicked', 'unpicked'), ('requested', 'requested'), ('received', 'received'), ('redeemed', 'redeemed'), ('paid', 'paid')], default='unpicked', max_length=30),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='made_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
