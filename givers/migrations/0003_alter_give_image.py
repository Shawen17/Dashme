# Generated by Django 3.2.8 on 2021-11-11 19:01

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0002_auto_20211108_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='give',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, size=[200, 200], upload_to=''),
        ),
    ]
