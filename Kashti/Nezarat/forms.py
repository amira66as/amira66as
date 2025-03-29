from django import forms
from django.forms import inlineformset_factory
from .models import (
    User, Part, CustomAttribute, Ship, ShipPart,
    TransportItem, Message, Company, TransportOperation
    , Warehouse, Reminder , TransportItem ,
    WarehouseSubStorage,ShipSubWarehouse,ShipAttribute ,
    PartAttribute , DamageReport
    )
from django.forms import modelformset_factory
class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label='نام کاربری')
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label='رمز عبور')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='تایید رمز عبور')
    company_code = forms.CharField(max_length=50, required=True, label='کد شرکت')
    profile_picture = forms.ImageField(required=False, label='عکس پروفایل')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'company_code', 'profile_picture', 'title')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمز عبور و تایید رمز عبور باید یکسان باشند.")
        return cleaned_data

class CompanyCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label='نام کاربری')
    name = forms.CharField(max_length=255, required=True, label='نام شرکت')
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label='رمز عبور')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='تایید رمز عبور')
    company_code = forms.CharField(max_length=50, required=True, label='کد شرکت')
    profile_picture = forms.ImageField(required=False, label='عکس پروفایل')

    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2', 'company_code', 'profile_picture')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمز عبور و تایید رمز عبور باید یکسان باشند.")
        return cleaned_data

class Choice(forms.ModelForm):
    position = forms.ChoiceField(choices=User.POSITION_CHOICE, label='انتخاب مقام', required=False)
    class Meta:
        model = User
        fields = ['position']

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = [
            'name',
            'image',
            'expiry_date',
            'quantity',
            'warehouse',
            'company_code',
            'warehouse_sub_storage',
            'ship_subwarehouse',
            'description',
            'storage_row',
            'storage_column',
            'storage_shelf',
            'is_consumable',
            'usage_limit_km',
        ]
        labels = {
            'name': 'نام قطعه',
            'image': 'تصویر',
            'expiry_date': 'تاریخ انقضا',
            'quantity': 'تعداد',
            'warehouse': 'انبار اصلی',
            'company_code': 'کد شرکت',
            'warehouse_sub_storage': 'زیرانبار',
            'ship_subwarehouse': 'زیرانبار کشتی',
            'description': 'توضیحات',
            'storage_row': 'ردیف',
            'storage_column': 'ستون',
            'storage_shelf': 'قفسه',
            'is_consumable': 'آیا این قطعه مصرفی است؟',
            'usage_limit_km': 'حداکثر مسافت قابل استفاده (کیلومتر)',
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                company = Company.objects.get(user=user)
                self.fields['warehouse'].queryset = Warehouse.objects.filter(company_code=company.company_code)
                self.fields['warehouse_sub_storage'].queryset = WarehouseSubStorage.objects.filter(warehouse__company_code=company.company_code)
            except Company.DoesNotExist:
                for f in self.fields:
                    if hasattr(self.fields[f], 'queryset'):
                        self.fields[f].queryset = Part.objects.none()


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = [
            'name', 
            'company_code', 
            'description', 
            'latitude', 
            'longitude',
            'image'
        ]
        labels = {
            'name': 'نام انبار',
            'company_code': 'کد شرکت',
            'description': 'توضیحات',
            'latitude': 'عرض جغرافیایی',
            'longitude': 'طول جغرافیایی',
            'image': ' عکس انبار',
        }


# با استفاده از inlineformset_factory یک formset برای زیرانبارها می‌سازیم:
WarehouseSubStorageFormSet = inlineformset_factory(
    Warehouse,
    WarehouseSubStorage,
    fields=['name', 'location_code', 'description'],
    extra=1,       # چند فرم خالی ابتدا نشان داده شود
    can_delete=True # اگر بخواهید کاربر بتواند بعضی زیرانبارها را حذف کند
)


class CustomAttributeForm(forms.ModelForm):
    class Meta:
        model = CustomAttribute
        fields = ['attribute_name', 'attribute_value']

class ShipForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True, label='مدل کشتی:')
    class Meta:
        model = Ship
        fields = ['name', 'description', 'image', 'company_code']

class ShipPartForm(forms.ModelForm):
    class Meta:
        model = ShipPart
        fields = ['ship', 'part', 'quantity']
    def __init__(self, *args, **kwargs):
        super(ShipPartForm, self).__init__(*args, **kwargs)

class SendMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.receiver = kwargs.pop('receiver', None)
        self.sender = kwargs.pop('sender', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        msg = super().save(commit=False)
        msg.sender = self.sender
        msg.receiver = self.receiver
        if commit:
            msg.save()
        return msg

           
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['reminder_type', 'reminder_date', 'note', 'company_code', 
                  'part', 'ship', 'warehouse', 'subwarehouse']
        labels = {
            'reminder_type': 'نوع یادآوری',
            'reminder_date': 'تاریخ یادآوری',
            'note': 'توضیحات یادآوری',
            'company_code': 'کد شرکت',
            'part': 'قطعه',
            'ship': 'کشتی',
            'warehouse': 'انبار',
            'subwarehouse': 'زیرانبار',
        }

        widgets = {
            'reminder_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReminderForm, self).__init__(*args, **kwargs)

        # همه فیلدهای ارتباطی اختیاری بشن
        self.fields['part'].required = False
        self.fields['ship'].required = False
        self.fields['warehouse'].required = False
        self.fields['subwarehouse'].required = False

        if user:
            try:
                company = Company.objects.get(user=user)
                self.fields['part'].queryset = Part.objects.filter(company_code=company.company_code)
                self.fields['ship'].queryset = Ship.objects.filter(company_code=company.company_code)
                self.fields['warehouse'].queryset = Warehouse.objects.filter(company_code=company.company_code)
                self.fields['subwarehouse'].queryset = WarehouseSubStorage.objects.filter(company_code=company.company_code)
            except Company.DoesNotExist:
                for field in ['part', 'ship', 'warehouse', 'subwarehouse']:
                    self.fields[field].queryset = Part.objects.none()
                    
class TransportOperationForm(forms.ModelForm):
    class Meta:
        model = TransportOperation
        fields = ['ship', 'from_warehouse', 'to_warehouse', 'distance_km', 'ship_speed_kph']
        labels = {
            'ship': 'کشتی',
            'from_warehouse': 'انبار مبدا',
            'to_warehouse': 'انبار مقصد',
            'distance_km': 'مسافت (کیلومتر)',
            'ship_speed_kph': 'سرعت کشتی (کیلومتر بر ساعت)',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                company = Company.objects.get(user=user)
                self.fields['ship'].queryset = Ship.objects.filter(company_code=company.company_code)
                self.fields['from_warehouse'].queryset = Warehouse.objects.filter(company_code=company.company_code)
                self.fields['to_warehouse'].queryset = Warehouse.objects.filter(company_code=company.company_code)
            except Company.DoesNotExist:
                for f in self.fields:
                    self.fields[f].queryset = Ship.objects.none()


# forms.py
class TransportItemForm(forms.ModelForm):
    part = forms.ModelChoiceField(queryset=Part.objects.all(), label="قطعه")
    quantity = forms.IntegerField(min_value=1, label="تعداد")

    class Meta:
        model = TransportItem
        fields = ['part', 'quantity', 'from_warehouse', 'to_subwarehouse', 'ship_subwarehouse', 'is_consumable', 'usage_percent', 'used_in_trip']
        labels = {
            'part': 'قطعه',
            'quantity': 'تعداد',
            'from_warehouse': 'انبار مبدا قطعه',
            'to_subwarehouse': 'زیرانبار مقصد',
            'is_consumable': 'آیا قطعه مصرفی است؟',
            'usage_percent': 'درصد استفاده در سفر',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                company = Company.objects.get(user=user)
                self.fields['part'].queryset = Part.objects.filter(company_code=company.company_code)
                self.fields['from_warehouse'].queryset = Warehouse.objects.filter(company_code=company.company_code)
                self.fields['to_subwarehouse'].queryset = WarehouseSubStorage.objects.filter(
    warehouse__company_code=company.company_code
)

            except Company.DoesNotExist:
                for f in self.fields:
                    self.fields[f].queryset = Part.objects.none()



TransportItemFormSet = modelformset_factory(
    TransportItem,
    form=TransportItemForm,
    extra=3,  # چند فرم خالی اولیه نشون داده بشه
    can_delete=True
)

class WarehouseSubStorageForm(forms.ModelForm):
    class Meta:
        model = WarehouseSubStorage
        fields = ['warehouse', 'name', 'description']
        labels = {
            'warehouse': 'انبار اصلی',
            'name': 'نام زیرانبار',
            'description': 'توضیحات اختیاری',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                company = Company.objects.get(user=user)
                self.fields['warehouse'].queryset = Warehouse.objects.filter(company_code=company.company_code)
            except Company.DoesNotExist:
                self.fields['warehouse'].queryset = Warehouse.objects.none()


class ShipSubWarehouseForm(forms.ModelForm):
    class Meta:
        model = ShipSubWarehouse
        fields = ['ship', 'name', 'description']
        labels = {
            'ship': 'کشتی',
            'name': 'نام زیرانبار',
            'description': 'توضیحات'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                company = Company.objects.get(user=user)
                self.fields['ship'].queryset = Ship.objects.filter(company_code=company.company_code)
            except Company.DoesNotExist:
                self.fields['ship'].queryset = Ship.objects.none()


class ShipAttributeForm(forms.ModelForm):
    class Meta:
        model = ShipAttribute
        fields = ['ship', 'attribute_name', 'attribute_value']
        labels = {
            'ship': 'کشتی',
            'attribute_name': 'نام ویژگی',
            'attribute_value': 'مقدار',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                company = Company.objects.get(user=user)
                self.fields['ship'].queryset = Ship.objects.filter(company_code=company.company_code)
            except Company.DoesNotExist:
                self.fields['ship'].queryset = Ship.objects.none()

class PartAttributeForm(forms.ModelForm):
    class Meta:
        model = PartAttribute
        fields = ['part', 'attribute_name', 'attribute_value']

class DamageReportForm(forms.ModelForm):
    class Meta:
        model = DamageReport
        fields = ['part', 'reason']
        labels = {
            'part': 'قطعه',
            'reason': 'توضیح خرابی',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                company = Company.objects.get(user=user)
                self.fields['part'].queryset = Part.objects.filter(company_code=company.company_code)
            except Company.DoesNotExist:
                self.fields['part'].queryset = Part.objects.none()

