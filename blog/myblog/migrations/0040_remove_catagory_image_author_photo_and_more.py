# Generated by Django 4.0 on 2022-01-11 02:23

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0039_photo_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catagory',
            name='image',
        ),
        migrations.AddField(
            model_name='author',
            name='photo',
            field=django_resized.forms.ResizedImageField(crop=None, default='author pic', force_format=None, keep_meta=True, quality=0, size=[200, 100], upload_to='authors'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myblog.catagory'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='info',
            field=models.TextField(default='**info empty**', help_text='editable caption info no reversable'),
        ),
    ]