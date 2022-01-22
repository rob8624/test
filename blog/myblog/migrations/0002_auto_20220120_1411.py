# Generated by Django 3.2.9 on 2022-01-20 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tile', models.CharField(default='Gallery', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.gallery'),
        ),
    ]