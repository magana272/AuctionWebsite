# Generated by Django 4.0.4 on 2022-05-30 00:51

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(upload_to=django.core.files.storage.FileSystemStorage(location='/auctions/images')),
        ),
    ]