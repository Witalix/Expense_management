# Generated by Django 5.0.1 on 2024-02-04 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_paymentmethod_last_added_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
