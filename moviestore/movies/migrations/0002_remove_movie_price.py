# Generated by Django 5.1.5 on 2025-02-04 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='price',
        ),
    ]
