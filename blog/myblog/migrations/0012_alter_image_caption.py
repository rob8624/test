# Generated by Django 4.0 on 2022-01-03 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0011_image_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='caption',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
