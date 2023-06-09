# Generated by Django 3.2.8 on 2021-10-29 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(blank=True, default='', max_length=15)),
                ('email', models.EmailField(max_length=150)),
                ('subject', models.CharField(choices=[('enquiry', 'Enquiry'), ('complaint', 'Complaint'), ('report', 'Report'), ('others', 'Others')], max_length=20)),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Give',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('lagos', 'Lagos'), ('ogun', 'Ogun'), ('osun', 'Osun'), ('oyo', 'Oyo'), ('ondo', 'Ondo'), ('kwara', 'Kwara'), ('niger', 'Niger'), ('nassarawa', 'Nassarawa'), ('plateau', 'Plateau'), ('abuja', 'Abuja'), ('edo', 'Edo'), ('abia', 'Abia'), ('akwa-ibom', 'Akwa-Ibom'), ('adamawa', 'Adamawa'), ('anambra', 'Anambra'), ('cross-river', 'Cross-River'), ('delta', 'Delta'), ('ebonyi', 'Ebonyi'), ('benue', 'Benue'), ('bayelsa', 'Bayelsa'), ('ekiti', 'Ekiti'), ('enugu', 'Enugu'), ('jigawa', 'Jigawa'), ('kano', 'Kano'), ('katsina', 'Katsina'), ('kogi', 'Kogi'), ('kebbi', 'Kebbi'), ('kaduna', 'Kaduna'), ('imo', 'Imo'), ('borno', 'Borno'), ('gombe', 'Gombe'), ('rivers', 'Rivers'), ('zamfara', 'Zamfara'), ('yobe', 'Yobe'), ('sokoto', 'Sokoto')], max_length=40)),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(blank=True, choices=[('furniture', 'Furniture'), ('clothe', 'Clothes'), ('shoe', 'Shoes'), ('toy', 'toys'), ('electronics', 'Electronics'), ('bags', 'Bags'), ('mobile', 'mobile-phones'), ('laptop', 'Laptops'), ('book', 'Books'), ('kitchen-utensils', 'Kitchen-utensils'), ('bicycle', 'Bicyle'), ('accessories', 'Accessories'), ('food-stuffs', 'Food-stuffs'), ('groceries', 'Groceries'), ('generator', 'Generator'), ('beauty-product', 'Beauty-product')], default='', max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('quantity', models.IntegerField()),
                ('giver_number', models.BigIntegerField(default='')),
                ('address', models.TextField(default='')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('date_requested', models.DateTimeField(blank=True, null=True)),
                ('date_received', models.DateTimeField(blank=True, null=True)),
                ('gift_recipient', models.CharField(blank=True, default='', max_length=100)),
                ('gift_status', models.CharField(blank=True, choices=[('unpicked', 'unpicked'), ('requested', 'requested'), ('received', 'received'), ('redeemed', 'redeemed')], default='unpicked', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='givers/images/')),
                ('state', models.CharField(choices=[('lagos', 'Lagos'), ('ogun', 'Ogun'), ('osun', 'Osun'), ('oyo', 'Oyo'), ('ondo', 'Ondo'), ('kwara', 'Kwara'), ('niger', 'Niger'), ('nassarawa', 'Nassarawa'), ('plateau', 'Plateau'), ('abuja', 'Abuja'), ('edo', 'Edo'), ('abia', 'Abia'), ('akwa-ibom', 'Akwa-Ibom'), ('adamawa', 'Adamawa'), ('anambra', 'Anambra'), ('cross-river', 'Cross-River'), ('delta', 'Delta'), ('ebonyi', 'Ebonyi'), ('benue', 'Benue'), ('bayelsa', 'Bayelsa'), ('ekiti', 'Ekiti'), ('enugu', 'Enugu'), ('jigawa', 'Jigawa'), ('kano', 'Kano'), ('katsina', 'Katsina'), ('kogi', 'Kogi'), ('kebbi', 'Kebbi'), ('kaduna', 'Kaduna'), ('imo', 'Imo'), ('borno', 'Borno'), ('gombe', 'Gombe'), ('rivers', 'Rivers'), ('zamfara', 'Zamfara'), ('yobe', 'Yobe'), ('sokoto', 'Sokoto')], default='', max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('request_date', models.DateTimeField(blank=True, null=True)),
                ('category', models.CharField(choices=[('furniture', 'Furniture'), ('clothe', 'Clothes'), ('shoe', 'Shoes'), ('toy', 'toys'), ('electronics', 'Electronics'), ('bags', 'Bags'), ('mobile', 'mobile-phones'), ('laptop', 'Laptops'), ('book', 'Books'), ('kitchen-utensils', 'Kitchen-utensils'), ('bicycle', 'Bicyle'), ('accessories', 'Accessories'), ('food-stuffs', 'Food-stuffs'), ('groceries', 'Groceries'), ('generator', 'Generator'), ('beauty-product', 'Beauty-product')], max_length=100)),
                ('giver_number', models.BigIntegerField(blank=True, null=True)),
                ('address', models.TextField(default='')),
                ('receiver_number', models.BigIntegerField(blank=True, null=True)),
                ('giver_contacted', models.BooleanField(default=False)),
                ('receiver_contacted', models.BooleanField(default=False)),
                ('delivery_address', models.TextField(blank=True, max_length=200, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('give', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gift', to='givers.give')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('made_on', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('checksum', models.CharField(blank=True, max_length=100, null=True)),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Received',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('date_received', models.DateTimeField(auto_now_add=True)),
                ('gift_requested', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='commodity', to='givers.give')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, default='', max_length=100)),
                ('lastname', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('state', models.CharField(choices=[('lagos', 'Lagos'), ('ogun', 'Ogun'), ('osun', 'Osun'), ('oyo', 'Oyo'), ('ondo', 'Ondo'), ('kwara', 'Kwara'), ('niger', 'Niger'), ('nassarawa', 'Nassarawa'), ('plateau', 'Plateau'), ('abuja', 'Abuja'), ('edo', 'Edo'), ('abia', 'Abia'), ('akwa-ibom', 'Akwa-Ibom'), ('adamawa', 'Adamawa'), ('anambra', 'Anambra'), ('cross-river', 'Cross-River'), ('delta', 'Delta'), ('ebonyi', 'Ebonyi'), ('benue', 'Benue'), ('bayelsa', 'Bayelsa'), ('ekiti', 'Ekiti'), ('enugu', 'Enugu'), ('jigawa', 'Jigawa'), ('kano', 'Kano'), ('katsina', 'Katsina'), ('kogi', 'Kogi'), ('kebbi', 'Kebbi'), ('kaduna', 'Kaduna'), ('imo', 'Imo'), ('borno', 'Borno'), ('gombe', 'Gombe'), ('rivers', 'Rivers'), ('zamfara', 'Zamfara'), ('yobe', 'Yobe'), ('sokoto', 'Sokoto')], max_length=50)),
                ('phone_number', models.BigIntegerField(default=8000000000)),
                ('sex', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default='', max_length=10)),
                ('profile_pic', models.ImageField(default='profiles/default_pic.jpg', upload_to='profiles')),
                ('bio', models.TextField(blank=True, default='')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GiveImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='givers/images/')),
                ('give', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='giveimage', to='givers.give')),
            ],
        ),
    ]
