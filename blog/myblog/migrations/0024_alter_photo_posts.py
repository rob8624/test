# Generated by Django 4.0 on 2022-01-06 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0023_alter_photo_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='posts',
            field=models.ManyToManyField(related_name='pictures', to='myblog.Post'),
        ),
    ]
