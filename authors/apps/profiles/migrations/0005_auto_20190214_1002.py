# Generated by Django 2.1.5 on 2019-02-14 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20190213_0936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='image_url',
        ),
    ]
