# Generated by Django 5.0.1 on 2024-05-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.CharField(blank=True, default='active', max_length=30, null=True),
        ),
    ]
