# Generated by Django 3.2.3 on 2021-05-19 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_product_items_details_product_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_items_details',
            name='product_items_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.products'),
        ),
        migrations.DeleteModel(
            name='Product_items',
        ),
    ]