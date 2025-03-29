# Generated by Django 5.1 on 2024-10-04 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nezarat', '0004_user_group_remove_user_groups_user_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='group',
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, choices=[('O', 'Operator'), ('S', 'SarShift'), ('C', 'Captain')], max_length=1),
        ),
    ]
