# Generated by Django 4.0 on 2022-01-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0031_alter_iptc_options_remove_iptc_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='feature_image',
        ),
        migrations.AddField(
            model_name='photo',
            name='feature_image',
            field=models.BooleanField(default=False),
        ),
    ]
