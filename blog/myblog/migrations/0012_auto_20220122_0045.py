# Generated by Django 3.2.9 on 2022-01-22 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0011_photo_albums'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='width',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]