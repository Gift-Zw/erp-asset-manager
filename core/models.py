from decimal import Decimal

from django.db import models
import datetime
from users.models import User
from datetime import date, timedelta
from django.urls import reverse

CURRENCIES = [
    ('USD', 'USD'),
    ('ZWL', 'ZWL')
]

DEPARTMENTS = [
    ('Software', 'Software'),
    ('Datacenter', 'Datacenter'),
    ('Technical Services', 'Technical Services'),
    ('Sales', 'Sales'),
    ('Finance and Admin', 'Finance and Admin')
]

Locations = [
    ('Software', 'Software'),
    ('Datacenter', 'Datacenter'),
    ('Kitchen', 'Kitchen'),
    ('Workshop', 'Workshop'),
    ('Boardroom', 'Boardroom'),
    ('Storeroom', 'Storeroom'),
    ('Sales', 'Sales'),
    ('Reception', 'Reception'),
    ('CEO Office', 'CEO Office'),
    ('Sales HOD', 'Sales HOD'),
    ('Software HOD', 'Software HOD'),
    ('Services HOD', 'Services HOD'),
    ('Finance HOD', 'Finance HOD'),
    ('Accounts Office', 'Accounts Office'),
    ('Workshop Admin', 'Workshop Admin'),
    ('Guest Toilet', 'Guest Toilet'),
    ('Workshop Toilet', 'Workshop Toilet'),
    ('Toilet', 'Toilet'),

]


class Vendor(models.Model):
    vendor_id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def edit_vendor(self):
        return reverse(
            'update-vendor',
            kwargs={
                'pk': self.vendor_id,
                'name': self.name
            }
        )

    def delete_vendor(self):
        return reverse('delete-vendor', kwargs={
            'id': self.vendor_id,

        })


class Asset(models.Model):
    asset_id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    purchase_value = models.DecimalField(decimal_places=2, max_digits=852)
    grv_number = models.CharField(max_length=255, unique=True)
    condition = models.CharField(max_length=255, default='NEW')
    date_purchased = models.DateField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    is_disposed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def days_used(self):
        diff = datetime.date.today().year - self.date_purchased.year
        return diff

    def dispose(self):
        self.is_disposed = True
        self.save()

    def dispose_asset(self):
        return reverse(
            'update-motor-vehicle',
            kwargs={
                'pk': self.asset_id,
                'grv': self.grv_number
            }
        )


class MotorVehicleDetail(models.Model):
    mvd_id = models.BigAutoField(primary_key=True, unique=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='vehicle_details')
    engine_number = models.CharField(max_length=80, unique=True)
    chassis_number = models.CharField(max_length=80, unique=True)
    duty = models.DecimalField(default=0, decimal_places=2, max_digits=80)
    freight = models.DecimalField(default=0, decimal_places=2, max_digits=25)
    reg_number = models.CharField(max_length=10, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Motor Vehicle"

    def __str__(self):
        return self.asset.name

    def edit_vehicle(self):
        return reverse(
            'update-motor-vehicle',
            kwargs={
                'pk': self.mvd_id,
                'reg_number': self.reg_number
            }
        )

    @property
    def total_cost(self):
        return self.asset.purchase_value + self.freight + self.duty

    @property
    def total_depreciation(self):
        value = self.asset.purchase_value * self.asset.days_used() * Decimal(0.2)
        return round(value, 2)

    @property
    def current_value(self):
        value = self.total_cost - self.total_depreciation
        if value > 0:
            return round(value, 2)
        else:
            return '0.00'


class FixtureAndFittingDetail(models.Model):
    ffd_id = models.BigAutoField(primary_key=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='fixture_details')
    asset_tag = models.CharField(max_length=100)
    room = models.CharField(max_length=255, default="KITCHEN")
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fixture and Fitting"

    def __str__(self):
        return self.asset.name

    def edit_fixture_fitting(self):
        return reverse(
            'update-fixture-fitting',
            kwargs={
                'pk': self.ffd_id,
                'asset_tag': self.asset_tag
            }
        )

    @property
    def total_depreciation(self):
        value = self.asset.purchase_value * self.asset.days_used() * Decimal(0.1)
        return round(value, 2)

    @property
    def current_value(self):
        value = self.asset.purchase_value - self.total_depreciation
        if value > 0:
            return value
        else:
            return '0.00'


class OfficeEquipmentDetail(models.Model):
    oed_id = models.BigAutoField(primary_key=True, unique=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='office_details')
    asset_tag = models.CharField(max_length=100, unique=True)
    room = models.CharField(max_length=255, default="Workshop")
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Office Equipment"

    def __str__(self):
        return self.asset.name

    def edit_office_equipment(self):
        return reverse(
            'update-office-equipment',
            kwargs={
                'pk': self.oed_id,
                'asset_tag': self.asset_tag
            }
        )

    @property
    def total_depreciation(self):
        value = self.asset.purchase_value * self.asset.days_used() * Decimal(0.1)
        return round(value, 2)

    @property
    def current_value(self):
        value = self.asset.purchase_value - self.total_depreciation
        if value > 0:
            return value
        else:
            return '0.00'


class DataCenterDetail(models.Model):
    dcd_id = models.BigAutoField(primary_key=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='datacenter_details')
    serial_number = models.CharField(max_length=100, unique=True)
    warranty_end = models.DateField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Datacenter Equipment"

    def __str__(self):
        return self.asset.name

    @property
    def is_warranty_active(self):
        return self.warranty_end > datetime.date.today()

    def edit_datacenter_equipment(self):
        return reverse(
            'update-datacenter-equip',
            kwargs={
                'pk': self.dcd_id,
                'serial_number': self.serial_number
            }
        )

    @property
    def total_depreciation(self):
        value = self.asset.purchase_value * self.asset.days_used() * Decimal(0.1)
        return round(value, 2)

    @property
    def current_value(self):
        value = self.asset.purchase_value - self.total_depreciation
        if value > 0:
            return value
        else:
            return '0.00'

    @property
    def warranty_days(self):
        diff = self.warranty_end - datetime.date.today()
        return diff.days


class ComputerEquipmentDetail(models.Model):
    ced_id = models.BigAutoField(primary_key=True, unique=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='computer_details')
    serial_number = models.CharField(max_length=100, unique=True)
    warranty_end = models.DateField(blank=True)
    room = models.CharField(max_length=255, default='SOFTWARE')
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Computer Equipment"

    def __str__(self):
        return self.asset.name

    def is_warranty_active(self):
        return self.warranty_end > datetime.date.today()

    def edit_computer_equipment(self):
        return reverse(
            'update-computer-equip',
            kwargs={
                'pk': self.ced_id,
                'serial_number': self.serial_number
            }
        )

    @property
    def warranty_days(self):
        diff = self.warranty_end - datetime.date.today()
        return diff.days

    @property
    def total_depreciation(self):
        value = self.asset.purchase_value * self.asset.days_used() * Decimal(0.1)
        return round(value, 2)

    @property
    def current_value(self):
        value = self.asset.purchase_value - self.total_depreciation
        if value > 0:
            return value
        else:
            return '0.00'


class Transfer(models.Model):
    transfer_id = models.BigAutoField(unique=True, primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transfers')
    transfer_to = models.CharField(max_length=100)
    transfer_from = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asset.name


class Repair(models.Model):
    repair_id = models.BigAutoField(primary_key=True, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='repairs')
    cost = models.DecimalField(decimal_places=2, max_digits=90)
    date = models.DateField()
    remarks = models.TextField(max_length=500)
    status = models.CharField(max_length=255, default='IN PROGRESS')
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asset.name


class Disposal(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='disposal')
    remarks = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asset.name
