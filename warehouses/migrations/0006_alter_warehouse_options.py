# Generated by Django 5.0.1 on 2024-05-22 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouses', '0005_alter_warehouseproduct_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='warehouse',
            options={'ordering': ['name', 'id']},
        ),
    ]