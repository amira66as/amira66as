# Generated by Django 5.1 on 2024-10-04 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Nezarat', '0006_rename_position_user_title_employee_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='TITLe',
            new_name='title',
        ),
    ]
