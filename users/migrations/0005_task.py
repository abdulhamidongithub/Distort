# Generated by Django 5.0.1 on 2024-03-28 04:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('status', models.CharField(max_length=30)),
                ('task_executor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bajaruvchi_tasklari', to=settings.AUTH_USER_MODEL)),
                ('task_setter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
