# Generated by Django 5.1 on 2024-10-04 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nezarat', '0002_alter_user_password_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
