# Generated by Django 5.1.6 on 2025-03-27 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nezarat', '0048_remove_employee_is_accepted_employee_assigned_ship_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippart',
            name='location_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
