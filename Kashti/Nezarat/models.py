from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    TITLE_CHOICE = [
        ('E', 'Employee'),
        ('C', 'Company'),
    ]
    POSITION_CHOICE = [
        ('U', 'Uncertain'),
        ('OA', 'OperatorA'),
        ('OB', 'OperatorB'),
        ('OS', 'OperatorS'),
        ('C', 'Captain'),
    ]
    position = models.CharField(max_length=2, choices=POSITION_CHOICE, blank=True, default='U')
    title = models.CharField(max_length=2, choices=TITLE_CHOICE, blank=True)

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    company_code = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام انبار")
    company_code = models.CharField(max_length=50, verbose_name="کد شرکت", default='UNKNOWN')
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='warehouse_pics/', null=True, blank=True, verbose_name="عکس انبار")

    def __str__(self):
        return self.name

class Ship(models.Model):
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(blank=True, null=True)
    company_code = models.CharField(max_length=50)
    image = models.ImageField(upload_to='kashti_pictures/Kashti/', blank=True, null=True)

    def __str__(self):
        return self.name

class ShipSubWarehouse(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='ship_sub_warehouses')
    name = models.CharField(max_length=100, verbose_name="نام زیرانبار کشتی")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)
    location_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="کد مکان (مثلاً C2-L1)")
    @property
    def parts(self):
        return self.transportitem_set.all()
    def __str__(self):
        return f"{self.name} ({self.ship.name})"
    


class WarehouseSubStorage(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام زیرانبار")
    warehouse = models.ForeignKey(
        Warehouse, 
        on_delete=models.CASCADE, 
        related_name='sub_storages'
    )
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)
    location_code = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="کد مکان (مثلاً R2-S3-A)"
    )

    def __str__(self):
        return f"{self.name} - {self.warehouse.name}"


class Part(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام قطعه")
    image = models.ImageField(upload_to='kashti_pictures/Part/', blank=True, null=True, verbose_name="تصویر")
    expiry_date = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ انقضا")
    quantity = models.PositiveIntegerField(default=0, verbose_name="تعداد")
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='parts', verbose_name="انبار")
    company_code = models.CharField(max_length=50, verbose_name="کد شرکت", default='UNKNOWN')  # این فیلد را اضافه کنید
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات کالا")

    warehouse_sub_storage = models.ForeignKey(
        WarehouseSubStorage,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="زیرانبار انبار"
    )
    ship_subwarehouse = models.ForeignKey(
        ShipSubWarehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="زیرانبار کشتی"
    )
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات کالا")  # این فیلد باید در مدل باشد
    storage_row = models.IntegerField(null=True, blank=True)
    storage_column = models.IntegerField(null=True, blank=True)
    storage_shelf = models.CharField(max_length=10, null=True, blank=True)


    is_consumable = models.BooleanField(default=False, verbose_name="قطعه مصرفی است؟")
    usage_limit_km = models.FloatField(blank=True, null=True, verbose_name="حداکثر مسافت قابل تحمل (کیلومتر)")
    is_worn_out = models.BooleanField(default=False, verbose_name="فرسوده شده؟")
    worn_out_reason = models.TextField(blank=True, null=True, verbose_name="دلیل فرسودگی")
    
    def get_status(self):
        if self.is_worn_out:
            return 'فرسوده شده است'
        elif self.expiry_date and self.expiry_date <= timezone.now().date():
            return 'منقضی'
        elif self.usage_limit_km:
            recent_item = self.transportitem_set.order_by('-operation__created_at').first()
            if recent_item and recent_item.usage_percent:
                used = (recent_item.usage_percent / 100) * recent_item.operation.distance_km
                if used >= self.usage_limit_km * 0.9:
                    return 'نزدیک فرسودگی'
        return 'سالم'

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_code = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='employee_pics/', null=True, blank=True)
    assigned_ship = models.ForeignKey(Ship, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.user.username

class Request(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class JobApplication(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=2, choices=User.POSITION_CHOICE, blank=True, default='U')
    status = models.CharField(max_length=20, default='Pending')
    # اگر می‌خواهید فلگ قبول/رد هم داشته باشید

    def __str__(self):
        return f"{self.employee.user.username} -> {self.company.name}"


class My_Employee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=2, choices=User.POSITION_CHOICE, blank=True, default='U')

    def __str__(self):
        return self.employee.user.username

class CustomAttribute(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='custom_attributes')
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=100)
    company_code = models.CharField(max_length=50, verbose_name="کد شرکت", default='DEFAULT_COMPANY_CODE')

class ShipPart(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name="ship_parts")
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    location_code = models.CharField(max_length=100, blank=True, null=True)  # فیلد جدید

    def __str__(self):
        return f"{self.part.name} on {self.ship.name}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.receiver.username

# مدل جدید برای Reminder (یادآوری)
class Reminder(models.Model):
    REMINDER_TYPE_CHOICES = [
        ('part', 'قطعه'),
        ('ship', 'کشتی'),
        ('Shipsubwarehouse', 'انبار سوار بر کشتی'),
        ('warehouse', 'انبار'),
        ('WarehouseSubStorage', 'زیرانبار'),
    ]

    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES, verbose_name="نوع یادآوری")
    reminder_date = models.DateTimeField(verbose_name="تاریخ یادآوری")
    note = models.TextField(blank=True, null=True, verbose_name="توضیحات یادآوری")
    company_code = models.CharField(max_length=50, verbose_name="کد شرکت")

    # اتصال‌های احتمالی
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, blank=True)
    ship = models.ForeignKey(Ship, on_delete=models.SET_NULL, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    subwarehouse = models.ForeignKey(WarehouseSubStorage, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_reminder_type_display()} - {self.reminder_date.strftime('%Y-%m-%d %H:%M')}"



class TransportOperation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'در حال بررسی'),
        ('IN_PROGRESS', 'در حال حرکت'),
        ('COMPLETED', 'انجام شده'),
        ('CANCELLED', 'لغو شده'),
    ]

    company_code = models.CharField(max_length=50, verbose_name="کد شرکت")
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, verbose_name="کشتی")
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="departure_operations", verbose_name="انبار مبدا")
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="arrival_operations", verbose_name="انبار مقصد")
    distance_km = models.FloatField(verbose_name="مسافت (کیلومتر)", help_text="می‌تونه دستی یا محاسبه‌شده باشه")
    ship_speed_kph = models.FloatField(verbose_name="سرعت کشتی (km/h)")
    estimated_duration_hr = models.FloatField(blank=True, null=True, verbose_name="مدت تخمینی سفر (ساعت)")
    is_approved_by_captain = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="وضعیت")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    started_at = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ شروع سفر")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ اتمام سفر")

    ship_subwarehouse = models.ForeignKey(ShipSubWarehouse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="زیرانبار کشتی")

    # محاسبه مدت زمان سفر
    def calculate_duration(self):
        if self.ship_speed_kph > 0:
            return round(self.distance_km / self.ship_speed_kph, 2)
        return None

    def save(self, *args, **kwargs):
        if self.estimated_duration_hr is None:
            self.estimated_duration_hr = self.calculate_duration()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.ship.name} | از {self.from_warehouse.name} به {self.to_warehouse.name}"

class TransportItem(models.Model):
    operation = models.ForeignKey(TransportOperation, on_delete=models.CASCADE, related_name='items')
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    # وضعیت قطعه
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    to_subwarehouse = models.ForeignKey(WarehouseSubStorage, on_delete=models.SET_NULL, null=True, blank=True)
    ship_subwarehouse = models.ForeignKey(ShipSubWarehouse, on_delete=models.SET_NULL, null=True, blank=True)
    
    # وضعیت مصرف قطعه در سفر
    is_consumable = models.BooleanField(default=False)  # آیا مصرف می‌شود؟
    usage_percent = models.FloatField(default=0)  # درصد استفاده از قطعه در سفر
    used_in_trip = models.BooleanField(default=False)  # آیا در این سفر مصرف می‌شود؟

    # وضعیت قطعه (فرسودگی یا انقضا)
    is_worn_out = models.BooleanField(default=False)

    def will_expire_during(self):
        """
        چک می‌کند آیا تاریخ انقضای قطعه تا قبل از اتمام این سفر فرا می‌رسد یا خیر.
        با فرض اینکه started_at خالی نباشد و سفر مدت‌زمانی تخمینی داشته باشد.
        """
        if self.part.expiry_date and self.operation.started_at and self.operation.estimated_duration_hr:
            arrival_time = self.operation.started_at + timedelta(hours=self.operation.estimated_duration_hr)
            return arrival_time >= self.part.expiry_date
        return False

    def will_wear_out_by_distance(self):
        """
        چک می‌کند آیا قطعه بر اساس usage_limit_km و usage_percent در طول سفر فرسوده می‌شود یا خیر.
        """
        if self.part.usage_limit_km and self.operation.distance_km and self.usage_percent:
            # مسافتی که از قطعه استفاده شده
            used_km = (self.usage_percent / 100) * self.operation.distance_km
            return used_km >= self.part.usage_limit_km
        return False

    def __str__(self):
        return f"{self.part.name} × {self.quantity}"


class ShipAttribute(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(max_length=100, verbose_name="نام ویژگی")
    attribute_value = models.CharField(max_length=255, verbose_name="مقدار ویژگی")

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"

class PartAttribute(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='part_attributes')
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"

class DamageReport(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='damage_reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'در انتظار'),
        ('CONFIRMED', 'تأیید شده'),
        ('REJECTED', 'رد شده')
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

