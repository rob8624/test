# Generated by Django 4.0 on 2022-01-04 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0015_image_lens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.CharField(editable=False, max_length=500),
        ),
    ]