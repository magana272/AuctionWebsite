# Generated by Django 3.2.5 on 2022-06-05 19:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_alter_listing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]