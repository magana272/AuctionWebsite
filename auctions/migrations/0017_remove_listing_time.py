# Generated by Django 4.0.4 on 2022-06-01 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_comment_time_alter_listing_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='time',
        ),
    ]
