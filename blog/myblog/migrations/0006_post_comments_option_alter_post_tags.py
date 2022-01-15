# Generated by Django 4.0 on 2021-12-27 17:13

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('myblog', '0005_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments_option',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='Use comma to separate', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Add Tags'),
        ),
    ]
