# Generated by Django 3.2.3 on 2021-07-07 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0032_auto_20210707_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorder',
            name='order_placed',
        ),
    ]
