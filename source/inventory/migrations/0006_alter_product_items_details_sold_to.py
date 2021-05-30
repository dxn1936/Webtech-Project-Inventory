# Generated by Django 3.2.3 on 2021-05-27 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_product_items_details_sold_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_items_details',
            name='sold_to',
            field=models.CharField(blank=True, choices=[('Ebay', 'Ebay'), ('Flipkart', 'Flipkart'), ('Amazon', 'Amazon')], max_length=50, null=True),
        ),
    ]
