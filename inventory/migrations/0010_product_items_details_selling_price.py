# Generated by Django 3.2.3 on 2021-05-19 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_product_items_details_sold_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_items_details',
            name='selling_price',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]