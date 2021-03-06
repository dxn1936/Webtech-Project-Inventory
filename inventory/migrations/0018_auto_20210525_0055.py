# Generated by Django 3.2.3 on 2021-05-24 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_alter_product_items_details_sold_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_reorder',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='product_items_details',
            name='sold_to',
            field=models.CharField(blank=True, choices=[('Ebay', 'Ebay'), ('Amazon', 'Amazon'), ('Flipkart', 'Flipkart')], max_length=50, null=True),
        ),
    ]
