# Generated by Django 3.1 on 2020-08-09 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date joined'),
        ),
    ]
