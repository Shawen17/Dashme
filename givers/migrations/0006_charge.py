# Generated by Django 3.2.8 on 2021-11-25 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0005_alter_transaction_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('charge', models.IntegerField()),
            ],
        ),
    ]
