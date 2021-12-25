# Generated by Django 4.0 on 2021-12-07 16:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique_for_date='publish')),
                ('body', models.CharField(max_length=5000)),
                ('summary', models.CharField(max_length=100)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('published', 'Published'), ('unpublished', 'Unpublished')], default='unpublished', max_length=50)),
                ('importance', models.CharField(choices=[('high', 'High'), ('medium', 'medium'), ('low', 'Low')], default='high', max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bog_posts', to='auth.user')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]