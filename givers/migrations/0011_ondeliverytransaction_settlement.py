# Generated by Django 3.2.8 on 2022-01-09 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0010_auto_20220108_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='ondeliverytransaction',
            name='settlement',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
