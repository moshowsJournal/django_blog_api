# Generated by Django 2.0.13 on 2020-08-08 10:37

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('full_name', models.CharField(max_length=100)),
                ('profile_photo', models.ImageField(null=True, upload_to=users.models.upload_location)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
