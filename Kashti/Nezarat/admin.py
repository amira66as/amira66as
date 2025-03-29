from django.contrib import admin
from . import models


class WarehouseSubStorageInline(admin.TabularInline):
    model = models.WarehouseSubStorage
    extra = 1  

@admin.register(models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست Warehouseها می‌بینید:
    list_display = ['name', 'company_code', 'description']
    # اضافه‌کردن اینلاین:
    inlines = [WarehouseSubStorageInline]


admin.site.register(models.User)
admin.site.register(models.Company)
admin.site.register(models.Employee)
admin.site.register(models.JobApplication)
admin.site.register(models.My_Employee)
admin.site.register(models.Part)
admin.site.register(models.CustomAttribute)
admin.site.register(models.ShipPart)
admin.site.register(models.Ship)
admin.site.register(models.Message)
admin.site.register(models.WarehouseSubStorage)