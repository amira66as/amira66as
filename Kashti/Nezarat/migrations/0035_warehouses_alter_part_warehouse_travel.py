# Generated by Django 5.1.2 on 2024-12-05 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nezarat', '0034_alter_company_company_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='part',
            name='warehouse',
            field=models.CharField(blank=True, choices=[('1', 'warhouse1'), ('2', 'warhouse2'), ('3', 'warhouse3'), ('4', 'warhouse4'), ('5', 'warhouse5'), ('6', 'warhouse6'), ('7', 'warhouse7'), ('8', 'warhouse8')], default='1', max_length=1),
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('from_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_warehouse', to='Nezarat.warehouses')),
                ('to_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_warehouse', to='Nezarat.warehouses')),
            ],
        ),
    ]
