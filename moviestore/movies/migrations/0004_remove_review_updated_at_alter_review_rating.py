# Generated by Django 5.1.6 on 2025-02-17 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_remove_order_movies_alter_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=1),
        ),
    ]
