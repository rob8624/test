# Generated by Django 4.0 on 2022-01-06 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0026_post_photos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='photos',
        ),
    ]