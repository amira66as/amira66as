# Generated by Django 5.1.6 on 2025-03-26 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nezarat', '0046_reminder_reminder_type_reminder_ship_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('is_consumable', models.BooleanField(default=False, verbose_name='مصرفی است؟')),
                ('usage_percent', models.FloatField(default=0, verbose_name='درصد استفاده در سفر')),
                ('is_worn_out', models.BooleanField(default=False, verbose_name='فرسوده شده؟')),
            ],
        ),
        migrations.CreateModel(
            name='TransportOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_code', models.CharField(max_length=50, verbose_name='کد شرکت')),
                ('distance_km', models.FloatField(help_text='می\u200cتونه دستی یا محاسبه\u200cشده باشه', verbose_name='مسافت (کیلومتر)')),
                ('ship_speed_kph', models.FloatField(verbose_name='سرعت کشتی (km/h)')),
                ('estimated_duration_hr', models.FloatField(blank=True, null=True, verbose_name='مدت تخمینی سفر (ساعت)')),
                ('is_approved_by_captain', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'در حال بررسی'), ('IN_PROGRESS', 'در حال حرکت'), ('COMPLETED', 'انجام شده'), ('CANCELLED', 'لغو شده')], default='PENDING', max_length=20, verbose_name='وضعیت')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ شروع سفر')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ اتمام سفر')),
            ],
        ),
        migrations.DeleteModel(
            name='Destination',
        ),
        migrations.RemoveField(
            model_name='travel',
            name='from_warehouse',
        ),
        migrations.RemoveField(
            model_name='travel',
            name='ship',
        ),
        migrations.RemoveField(
            model_name='travel',
            name='to_warehouse',
        ),
        migrations.RemoveField(
            model_name='travelpart',
            name='travel',
        ),
        migrations.RemoveField(
            model_name='reminder',
            name='travel',
        ),
        migrations.RemoveField(
            model_name='travelpart',
            name='part',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='reminder_type',
            field=models.CharField(choices=[('part', 'قطعه'), ('ship', 'کشتی'), ('warehouse', 'انبار'), ('subwarehouse', 'زیرانبار')], max_length=20, verbose_name='نوع یادآوری'),
        ),
        migrations.AddField(
            model_name='transportitem',
            name='from_warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_sources', to='Nezarat.warehouse'),
        ),
        migrations.AddField(
            model_name='transportitem',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Nezarat.part'),
        ),
        migrations.AddField(
            model_name='transportitem',
            name='to_subwarehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_destinations', to='Nezarat.subwarehouse'),
        ),
        migrations.AddField(
            model_name='transportoperation',
            name='from_warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_operations', to='Nezarat.warehouse', verbose_name='انبار مبدا'),
        ),
        migrations.AddField(
            model_name='transportoperation',
            name='ship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Nezarat.ship', verbose_name='کشتی'),
        ),
        migrations.AddField(
            model_name='transportoperation',
            name='to_warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_operations', to='Nezarat.warehouse', verbose_name='انبار مقصد'),
        ),
        migrations.AddField(
            model_name='transportitem',
            name='operation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Nezarat.transportoperation'),
        ),
        migrations.DeleteModel(
            name='Shipment',
        ),
        migrations.DeleteModel(
            name='Travel',
        ),
        migrations.DeleteModel(
            name='TravelPart',
        ),
    ]
