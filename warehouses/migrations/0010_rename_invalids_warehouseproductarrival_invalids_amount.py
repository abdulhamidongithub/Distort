# Generated by Django 5.0.1 on 2024-05-27 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouses', '0009_warehouseproductarrival_invalids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='warehouseproductarrival',
            old_name='invalids',
            new_name='invalids_amount',
        ),
    ]