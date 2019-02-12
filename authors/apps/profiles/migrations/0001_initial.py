# Generated by Django 2.1.5 on 2019-02-14 10:35

import cloudinary.models
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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('image_url', cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dy2faavdk/image/upload/v1548264034/qvxtpdmi03kksg9rxgfj.png', max_length=255, verbose_name='image')),
                ('company', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=250)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
