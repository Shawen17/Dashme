# Generated by Django 3.2.8 on 2022-04-16 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0012_auto_20220410_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='ticket',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
