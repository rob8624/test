# Generated by Django 4.0 on 2022-01-04 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0016_alter_image_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='caption',
            field=models.CharField(default='Caption info', editable=False, max_length=500),
        ),
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
