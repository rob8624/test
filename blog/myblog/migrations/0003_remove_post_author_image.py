# Generated by Django 4.0 on 2021-12-09 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_author_remove_post_importance_post_author_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author_image',
        ),
    ]