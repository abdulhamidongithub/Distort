# Generated by Django 5.0.1 on 2024-05-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_driverlocation_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='driver_device_token',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
