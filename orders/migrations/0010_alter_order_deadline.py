# Generated by Django 5.0.1 on 2024-05-02 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_kpiearning_amount_alter_order_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]