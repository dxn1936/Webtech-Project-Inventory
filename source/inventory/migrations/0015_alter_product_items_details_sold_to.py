# Generated by Django 3.2.3 on 2021-05-24 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20210524_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_items_details',
            name='sold_to',
            field=models.CharField(blank=True, choices=[('Amazon', 'Amazon'), ('Flipkart', 'Flipkart'), ('Ebay', 'Ebay')], max_length=50, null=True),
        ),
    ]
