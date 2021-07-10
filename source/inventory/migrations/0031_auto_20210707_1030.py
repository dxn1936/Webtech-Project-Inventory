# Generated by Django 3.2.3 on 2021-07-07 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0030_auto_20210707_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='order_total_amt',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=19),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_height_cm',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=19),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_length_cm',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=19),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_weight_g',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=19),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_width_cm',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=19),
        ),
        migrations.AlterField(
            model_name='rack',
            name='available_storage_vol',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=19),
        ),
        migrations.AlterField(
            model_name='rack',
            name='total_storage_vol',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=19),
        ),
    ]
