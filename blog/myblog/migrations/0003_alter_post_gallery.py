# Generated by Django 3.2.9 on 2022-01-20 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20220120_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='gallery',
            field=models.ForeignKey(default='24', on_delete=django.db.models.deletion.CASCADE, to='myblog.gallery'),
        ),
    ]