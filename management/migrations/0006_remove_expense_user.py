# Generated by Django 5.0.1 on 2024-02-04 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_category_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='user',
        ),
    ]
