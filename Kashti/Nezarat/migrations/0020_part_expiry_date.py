# Generated by Django 5.1.1 on 2024-10-09 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nezarat', '0019_kashti_part_travel_feature'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
