# Generated by Django 5.1.3 on 2024-12-04 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nezarat', '0033_rename_registration_code_company_company_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_code',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
