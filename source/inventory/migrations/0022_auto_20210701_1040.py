# Generated by Django 3.2.3 on 2021-07-01 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_auto_20210530_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rack',
            name='capacity',
        ),
        migrations.AddField(
            model_name='products',
            name='product_height_cm',
            field=models.DecimalField(decimal_places=10, default='0', max_digits=19),
        ),
        migrations.AddField(
            model_name='products',
            name='product_length_cm',
            field=models.DecimalField(decimal_places=10, default='0', max_digits=19),
        ),
        migrations.AddField(
            model_name='products',
            name='product_weight_g',
            field=models.DecimalField(decimal_places=10, default='0', max_digits=19),
        ),
        migrations.AddField(
            model_name='products',
            name='product_width_cm',
            field=models.DecimalField(decimal_places=10, default='0', max_digits=19),
        ),
        migrations.AddField(
            model_name='rack',
            name='available_storage_vol',
            field=models.DecimalField(decimal_places=10, default='0', max_digits=19),
        ),
        migrations.AddField(
            model_name='rack',
            name='total_storage_vol',
            field=models.DecimalField(decimal_places=10, default='0', max_digits=19),
        ),
    ]