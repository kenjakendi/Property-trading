# Generated by Django 4.2.1 on 2023-06-14 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_remove_property_is_sold_property_for_sale_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.BigIntegerField(),
        ),
    ]
