# Generated by Django 3.1.5 on 2021-01-15 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper_backend', '0002_instagramuser_hash_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramuser',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instagramuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
