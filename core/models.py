from decimal import Decimal
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils.text import slugify
from users.models import User
from django.urls import reverse

ASSET_SOURCES = [
    ('PURCHASED', 'PURCHASED'),
    ('DONATED', 'DONATED'),
    ('FORFEITED', 'FORFEITED')
]


class TimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AssetClassProperties(TimeStampedModel):
    name = models.CharField(max_length=255)
    depreciation_rate = models.DecimalField(max_digits=30, decimal_places=2)

    def __str__(self):
        return self.name


class Room(TimeStampedModel):
    room_id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=250)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Department(TimeStampedModel):
    department_id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=250)
    is_deleted = models.BooleanField(default=False)


class Vendor(models.Model):
    vendor_id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def edit_vendor(self):
        return reverse('update-vendor', kwargs={'pk': self.vendor_id, 'name': self.name})

    def delete_vendor(self):
        return reverse('delete-vendor', kwargs={'id': self.vendor_id})


class BaseAsset(models.Model):
    asset_id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    useful_life = models.PositiveIntegerField(blank=True, default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=852)
    source = models.CharField(max_length=255, default='PURCHASED')
    purchase_date = models.DateField()
    last_depreciation_date = models.DateField(blank=True, null=True)
    accumulated_depreciation = models.DecimalField(max_digits=30, decimal_places=2, default=0, blank=True)
    is_disposed = models.BooleanField(default=False)
    pending_disposal = models.BooleanField(default=False)
    asset_class = models.ForeignKey(AssetClassProperties, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def months_used(self):
        current_date = datetime.date.today()
        months_in_use = (current_date.year - self.purchase_date.year) * 12 + (
                current_date.month - self.purchase_date.month)
        return int(months_in_use)

    @property
    def years_used(self):
        current_date = datetime.date.today()
        years_in_use = current_date.year - self.purchase_date.year
        if current_date.month < self.purchase_date.month or (
                current_date.month == self.purchase_date.month and current_date.day < self.purchase_date.day):
            years_in_use -= 1
        return years_in_use

    @property
    def net_book_value(self):
        return self.cost - self.get_accumulated_depreciation

    @property
    def annual_depreciation(self):
        annual_depreciation = self.cost * self.asset_class.depreciation_rate
        return annual_depreciation

    @property
    def get_accumulated_depreciation(self):
        accumulated_depreciation = self.annual_depreciation * self.months_used / 12
        return accumulated_depreciation

    def calculate_accumulated_depreciation(self, depreciation_period):
        depreciation = self.annual_depreciation * (depreciation_period / 12)
        return depreciation

    class Meta:
        abstract = True


class Land(BaseAsset):
    area = models.DecimalField(max_digits=10, decimal_places=2)
    land_type = models.CharField(max_length=50)
    title_deed_number = models.CharField(max_length=50, unique=True)
    title_deed = models.FileField(upload_to='title deeds/', blank=True)
    registered_owner = models.CharField(max_length=255)

    def dispose_land(self, disposal_date, disposal_type, disposal_price, reason, attachment1=None, attachment2=None):
        disposal = AssetDisposal.objects.create(
            asset=self,
            disposal_date=disposal_date,
            disposal_type=disposal_type,
            disposal_price=disposal_price,
            reason=reason,
            attachment1=attachment1,
            attachment2=attachment2
        )
        self.is_disposed = True
        self.save()
        return disposal

    def transfer_land(self, transfer_to, transfer_from, remarks):
        transfer = AssetTransfer.objects.create(
            asset=self,
            transfer_to=transfer_to,
            transfer_from=transfer_from,
            remarks=remarks
        )
        transfer.save()
        return transfer

    def edit_land(self):
        return reverse(
            'land-update',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def dispose(self):
        return reverse(
            'land-dispose',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def revalue_asset(self, new_value, remarks, userName):
        old_value = self.net_book_value
        accumulated_dep = self.get_accumulated_depreciation
        diff = self.net_book_value - new_value
        old_date_purchased = self.purchase_date

        self.purchase_date = datetime.date.today()
        self.cost = new_value
        self.save()

        record = AssetRevaluationRecord.objects.create(
            new_value=new_value,
            old_value=old_value,
            accumulated_depreciation=accumulated_dep,
            asset_purchase_date=old_date_purchased,
            remarks=remarks,
            perfomed_by=userName

        )


class Building(BaseAsset):
    address = models.CharField(max_length=255)
    construction_date = models.DateField()
    floor_area = models.DecimalField(max_digits=10, decimal_places=2)
    building_type = models.CharField(max_length=50)
    number_of_floors = models.PositiveIntegerField()

    def dispose_building(self, disposal_date, disposal_type, disposal_price, reason, attachment1=None,
                         attachment2=None):
        disposal = AssetDisposal.objects.create(
            asset=self,
            disposal_date=disposal_date,
            disposal_price=disposal_price,
            disposal_type=disposal_type,
            reason=reason,
            attachment1=attachment1,
            attachment2=attachment2
        )
        self.is_disposed = True
        self.save()
        return disposal

    def repair_building(self, repair_date, repair_cost, description, status="Pending Approval", repair_quote=None, ):
        repair = AssetRepair.objects.create(
            asset=self,
            repair_date=repair_date,
            repair_cost=repair_cost,
            description=description,
            status=status,
            repair_quote=repair_quote
        )
        repair.save()
        return repair

    def transfer_building(self, transfer_date, transfer_to, transfer_from, remarks):
        transfer = AssetTransfer.objects.create(
            asset=self,
            transfer_to=transfer_to,
            transfer_from=transfer_from,
            remarks=remarks,
            transfer_date=transfer_date
        )
        transfer.save()
        return transfer

    def edit_building(self):
        return reverse(
            'building-update',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def dispose(self):
        return reverse(
            'building-dispose',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def repair(self):
        return reverse(
            'building-repair',
            kwargs={
                'pk': self.asset_id
            }
        )

    def transfer(self):
        return reverse(
            'building-transfer',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def revalue_asset(self, new_value, remarks, userName):
        old_value = self.net_book_value
        accumulated_dep = self.get_accumulated_depreciation
        diff = self.net_book_value - new_value
        old_date_purchased = self.purchase_date

        self.purchase_date = datetime.date.today()
        self.cost = new_value
        self.save()

        record = AssetRevaluationRecord.objects.create(
            new_value=new_value,
            old_value=old_value,
            accumulated_depreciation=accumulated_dep,
            asset_purchase_date=old_date_purchased,
            remarks=remarks,
            perfomed_by=userName

        )


class MotorVehicle(BaseAsset):
    duty = models.DecimalField(default=0, decimal_places=2, max_digits=80)
    freight = models.DecimalField(default=0, decimal_places=2, max_digits=25)
    registration_number = models.CharField(max_length=20)
    engine_number = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.PositiveIntegerField()

    @property
    def total_cost(self):
        return self.freight + self.duty + self.cost

    def dispose_motor_vehicle(self, disposal_date, disposal_type, disposal_price, reason, attachment1=None,
                              attachment2=None):
        disposal = AssetDisposal.objects.create(
            asset=self,
            disposal_date=disposal_date,
            disposal_price=disposal_price,
            disposal_type=disposal_type,
            reason=reason,
            attachment1=attachment1,
            attachment2=attachment2
        )
        self.is_disposed = True
        self.save()
        return disposal

    def repair_motor_vehicle(self, repair_date, repair_cost, description, status="Pending Approval",
                             repair_quote=None, ):
        repair = AssetRepair.objects.create(
            asset=self,
            repair_date=repair_date,
            repair_cost=repair_cost,
            description=description,
            status=status,
            repair_quote=repair_quote
        )
        repair.save()
        return repair

    def transfer_motor_vehicle(self, transfer_date, transfer_to, transfer_from, remarks):
        transfer = AssetTransfer.objects.create(
            asset=self,
            transfer_to=transfer_to,
            transfer_from=transfer_from,
            remarks=remarks,
            transfer_date=transfer_date
        )
        transfer.save()
        return transfer

    def edit_moto_vehicles(self):
        return reverse(
            'motor-vehicle-update',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def dispose(self):
        return reverse(
            'motor-vehicle-dispose',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def repair(self):
        return reverse(
            'motor-vehicle-repair',
            kwargs={
                'pk': self.asset_id
            }
        )

    def transfer(self):
        return reverse(
            'motor-vehicle-transfer',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def revalue_asset(self, new_value, remarks, userName):
        old_value = self.net_book_value
        accumulated_dep = self.get_accumulated_depreciation
        diff = self.net_book_value - new_value
        old_date_purchased = self.purchase_date

        self.purchase_date = datetime.date.today()
        self.cost = new_value
        self.save()

        record = AssetRevaluationRecord.objects.create(
            new_value=new_value,
            old_value=old_value,
            accumulated_depreciation=accumulated_dep,
            asset_purchase_date=old_date_purchased,
            remarks=remarks,
            perfomed_by=userName

        )


class Machinery(BaseAsset):
    serial_number = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    capacity = models.CharField(max_length=50)

    def dispose_machinery(self, disposal_date, disposal_type, disposal_price, reason, attachment1=None,
                          attachment2=None):
        disposal = AssetDisposal.objects.create(
            asset=self,
            disposal_date=disposal_date,
            disposal_price=disposal_price,
            disposal_type=disposal_type,
            reason=reason,
            attachment1=attachment1,
            attachment2=attachment2
        )
        self.is_disposed = True
        self.save()
        return disposal

    def repair_machinery(self, repair_date, repair_cost, description, status="Pending Approval", repair_quote=None, ):
        repair = AssetRepair.objects.create(
            asset=self,
            repair_date=repair_date,
            repair_cost=repair_cost,
            description=description,
            status=status,
            repair_quote=repair_quote
        )
        repair.save()
        return repair

    def transfer_machinery(self, transfer_date, transfer_to, transfer_from, remarks):
        transfer = AssetTransfer.objects.create(
            asset=self,
            transfer_to=transfer_to,
            transfer_from=transfer_from,
            remarks=remarks,
            transfer_date=transfer_date
        )
        transfer.save()
        return transfer

    def edit_machinery(self):
        return reverse(
            'machinery-update',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def dispose(self):
        return reverse(
            'machinery-dispose',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def repair(self):
        return reverse(
            'machinery-repair',
            kwargs={
                'pk': self.asset_id
            }
        )

    def transfer(self):
        return reverse(
            'machinery-transfer',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def revalue_asset(self, new_value, remarks, userName):
        old_value = self.net_book_value
        accumulated_dep = self.get_accumulated_depreciation
        diff = self.net_book_value - new_value
        old_date_purchased = self.purchase_date

        self.purchase_date = datetime.date.today()
        self.cost = new_value
        self.save()

        record = AssetRevaluationRecord.objects.create(
            new_value=new_value,
            old_value=old_value,
            accumulated_depreciation=accumulated_dep,
            asset_purchase_date=old_date_purchased,
            remarks=remarks,
            perfomed_by=userName

        )


class Furniture(BaseAsset):
    asset_tag = models.CharField(max_length=100, unique=True)
    material = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)

    def dispose_furniture(self, disposal_date, disposal_type, disposal_price, reason, attachment1=None,
                          attachment2=None):
        disposal = AssetDisposal.objects.create(
            asset=self,
            disposal_date=disposal_date,
            disposal_price=disposal_price,
            disposal_type=disposal_type,
            reason=reason,
            attachment1=attachment1,
            attachment2=attachment2
        )
        self.is_disposed = True
        self.save()
        return disposal

    def repair_furniture(self, repair_date, repair_cost, description, status="Pending Approval", repair_quote=None, ):
        repair = AssetRepair.objects.create(
            asset=self,
            repair_date=repair_date,
            repair_cost=repair_cost,
            description=description,
            status=status,
            repair_quote=repair_quote
        )
        repair.save()
        return repair

    def transfer_furniture(self, transfer_date, transfer_to, transfer_from, remarks):
        transfer = AssetTransfer.objects.create(
            asset=self,
            transfer_to=transfer_to,
            transfer_from=transfer_from,
            remarks=remarks,
            transfer_date=transfer_date
        )
        transfer.save()
        return transfer

    def edit_furniture(self):
        return reverse(
            'furniture-update',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def dispose(self):
        return reverse(
            'furniture-dispose',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def repair(self):
        return reverse(
            'furniture-repair',
            kwargs={
                'pk': self.asset_id
            }
        )

    def transfer(self):
        return reverse(
            'furniture-transfer',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def revalue_asset(self, new_value, remarks, userName):
        old_value = self.net_book_value
        accumulated_dep = self.get_accumulated_depreciation
        diff = self.net_book_value - new_value
        old_date_purchased = self.purchase_date

        self.purchase_date = datetime.date.today()
        self.cost = new_value
        self.save()

        record = AssetRevaluationRecord.objects.create(
            new_value=new_value,
            old_value=old_value,
            accumulated_depreciation=accumulated_dep,
            asset_purchase_date=old_date_purchased,
            remarks=remarks,
            perfomed_by=userName

        )


class Equipment(BaseAsset):
    serial_number = models.CharField(max_length=50, unique=True)
    manufacturer = models.CharField(max_length=255)
    asset_tag = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def dispose_equipment(self, disposal_date, disposal_type, disposal_price, reason, attachment1=None,
                          attachment2=None):
        disposal = AssetDisposal.objects.create(
            asset=self,
            disposal_date=disposal_date,
            disposal_price=disposal_price,
            disposal_type=disposal_type,
            reason=reason,
            attachment1=attachment1,
            attachment2=attachment2
        )
        self.is_disposed = True
        self.save()
        return disposal

    def repair_equipment(self, repair_date, repair_cost, description, status="Pending Approval", repair_quote=None, ):
        repair = AssetRepair.objects.create(
            asset=self,
            repair_date=repair_date,
            repair_cost=repair_cost,
            description=description,
            status=status,
            repair_quote=repair_quote
        )
        repair.save()
        return repair

    def transfer_equipment(self, transfer_date, transfer_to, transfer_from, remarks):
        transfer = AssetTransfer.objects.create(
            asset=self,
            transfer_to=transfer_to,
            transfer_from=transfer_from,
            remarks=remarks,
            transfer_date=transfer_date
        )
        transfer.save()
        return transfer

    def edit_equipment(self):
        return reverse(
            'equipment-update',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def dispose(self):
        return reverse(
            'equipment-dispose',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def repair(self):
        return reverse(
            'equipment-repair',
            kwargs={
                'pk': self.asset_id
            }
        )

    def transfer(self):
        return reverse(
            'equipment-transfer',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def revalue_asset(self, new_value, remarks, userName):
        old_value = self.net_book_value
        accumulated_dep = self.get_accumulated_depreciation
        diff = self.net_book_value - new_value
        old_date_purchased = self.purchase_date

        self.purchase_date = datetime.date.today()
        self.cost = new_value
        self.save()

        record = AssetRevaluationRecord.objects.create(
            asset=self,
            new_value=new_value,
            old_value=old_value,
            accumulated_depreciation=accumulated_dep,
            asset_purchase_date=old_date_purchased,
            remarks=remarks,
            perfomed_by=userName

        )


class Fixture(BaseAsset):
    asset_tag = models.CharField(max_length=100)
    location = models.ForeignKey(Room, on_delete=models.CASCADE)

    def dispose_fixture(self, disposal_date, disposal_type, disposal_price, reason, attachment1=None, attachment2=None):
        disposal = AssetDisposal.objects.create(
            asset=self,
            disposal_date=disposal_date,
            disposal_price=disposal_price,
            disposal_type=disposal_type,
            reason=reason,
            attachment1=attachment1,
            attachment2=attachment2
        )
        self.is_disposed = True
        self.save()
        return disposal

    def repair_fixture(self, repair_date, repair_cost, description, status="Pending Approval", repair_quote=None, ):
        repair = AssetRepair.objects.create(
            asset=self,
            repair_date=repair_date,
            repair_cost=repair_cost,
            description=description,
            status=status,
            repair_quote=repair_quote
        )
        repair.save()
        return repair

    def transfer_fixture(self, transfer_date, transfer_to, transfer_from, remarks):
        transfer = AssetTransfer.objects.create(
            asset=self,
            transfer_to=transfer_to,
            transfer_from=transfer_from,
            remarks=remarks,
            transfer_date=transfer_date
        )
        transfer.save()
        return transfer

    def edit_fixture(self):
        return reverse(
            'fixture-update',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def dispose(self):
        return reverse(
            'fixture-dispose',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def repair(self):
        return reverse(
            'fixture-repair',
            kwargs={
                'pk': self.asset_id
            }
        )

    def transfer(self):
        return reverse(
            'fixture-transfer-transfer',
            kwargs={
                'pk': self.asset_id,
            }
        )

    def revalue_asset(self, new_value, remarks, userName):
        old_value = self.net_book_value
        accumulated_dep = self.get_accumulated_depreciation
        diff = self.net_book_value - new_value
        old_date_purchased = self.purchase_date

        self.purchase_date = datetime.date.today()
        self.cost = new_value
        self.save()

        record = AssetRevaluationRecord.objects.create(
            new_value=new_value,
            old_value=old_value,
            accumulated_depreciation=accumulated_dep,
            asset_purchase_date=old_date_purchased,
            remarks=remarks,
            perfomed_by=userName

        )


class AssetDisposal(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')
    disposal_type = models.CharField(max_length=255, )
    disposal_date = models.DateField()
    disposal_price = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(max_length=255)
    attachment1 = models.FileField(upload_to='disposals/', blank=True)
    attachment2 = models.FileField(upload_to='disposals/', blank=True)
    approved = models.BooleanField(default=False)
    approved_date = models.DateTimeField(blank=True, null=True)
    approvedBy = models.CharField(max_length=250, blank=True)
    is_rejected = models.BooleanField(default=False)

    def approve_disposal(self, approvedBy):
        self.approved = True
        self.approved_date = datetime.datetime.now()
        self.approvedBy = approvedBy
        self.asset.is_disposed = True
        self.asset.save()
        self.save()

    def reject_disposal(self, approvedBy):
        self.is_rejected = True
        self.approved_date = datetime.datetime.now()
        self.approvedBy = approvedBy
        self.asset.save()
        self.save()


class AssetRepair(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')
    repair_date = models.DateField()
    repair_cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=250, default='Pending Approval')
    repair_quote = models.FileField(upload_to='repairs/', blank=True)
    approved = models.BooleanField(default=False)
    approved_date = models.DateTimeField(blank=True, null=True)
    approvedBy = models.CharField(max_length=250, blank=True)
    is_rejected = models.BooleanField(default=False)

    def approve_repair(self, approvedBy):
        self.approved = True
        self.approved_date = datetime.datetime.now()
        self.approvedBy = approvedBy
        self.save()

    def rejected_repair(self, approvedBy):
        self.is_rejected = True
        self.approved_date = datetime.datetime.now()
        self.approvedBy = approvedBy
        self.save()


class DepreciationEntry(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')
    depreciation_date = models.DateField()
    depreciation_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.asset.accumulated_depreciation += self.depreciation_amount
        self.asset.last_depreciation_date = datetime.date.today()
        self.asset.save()


class AssetTransfer(TimeStampedModel):
    transfer_id = models.BigAutoField(unique=True, primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')
    transfer_to = models.CharField(max_length=100)
    transfer_from = models.CharField(max_length=100)
    transfer_date = models.DateField()
    approved_date = models.DateField(blank=True, null=True)
    approved_by = models.CharField(max_length=255, default='')
    remarks = models.TextField(max_length=500, blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.asset.name

    def approve_transfer(self, approvedBy):
        self.is_approved = True
        self.approved_date = datetime.datetime.now()
        self.approved_by = approvedBy
        self.save()

    def reject_transfer(self, rejectedBy):
        self.is_rejected = True
        self.approve_transfer = datetime.datetime.now()
        self.approved_by = rejectedBy
        self.save()


class AssetRevaluationRecord(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')
    old_value = models.DecimalField(decimal_places=2, max_digits=85)
    new_value = models.DecimalField(decimal_places=2, max_digits=85)
    accumulated_depreciation = models.DecimalField(decimal_places=2, max_digits=85)
    remarks = models.TextField(max_length=500)
    asset_purchase_date = models.DateField()
    perfomed_by = models.CharField(max_length=255)

#
#
# class Room(models.Model):
#     room_id = models.BigAutoField(primary_key=True, unique=True)
#     name = models.CharField(max_length=250)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=False)
#
#
# class Department(models.Model):
#     department_id = models.BigAutoField(primary_key=True, unique=True)
#     name = models.CharField(max_length=250)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=False)
#
#
# class Vendor(models.Model):
#     vendor_id = models.BigAutoField(primary_key=True, unique=True)
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     address_line = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     def edit_vendor(self):
#         return reverse(
#             'update-vendor',
#             kwargs={
#                 'pk': self.vendor_id,
#                 'name': self.name
#             }
#         )
#
#     def delete_vendor(self):
#         return reverse('delete-vendor', kwargs={
#             'id': self.vendor_id,
#
#         })
#
#
# class BaseAsset(models.Model):
#     asset_id = models.BigAutoField(primary_key=True, unique=True)
#     slug = models.SlugField(unique=True, blank=True)
#     name = models.CharField(max_length=255)
#     useful_life = models.PositiveIntegerField()
#     cost = models.DecimalField(decimal_places=2, max_digits=852)
#     purchase_date = models.DateField()
#     depreciation_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     depreciation_method = models.CharField(max_length=50, choices=DEPRECIATION_METHODS)
#     last_depreciation_date = models.DateField(blank=True)
#     accumulated_depreciation = models.DecimalField(max_digits=30, decimal_places=2, default=0)
#     is_disposed = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True
#
#     def __str__(self):
#         return self.name
#
#     def calculate_depreciation(self):
#         if self.depreciation_method == 'straight_line':
#             return straight_line_depreciation(self.cost, self.useful_life)
#         elif self.depreciation_method == 'reducing_balance':
#             return reducing_balance_depreciation(self.cost, self.useful_life, self.depreciation_rate)
#         elif self.depreciation_method == 'units_of_production':
#             return units_of_production_depreciation(self.cost, self.useful_life, self.depreciation_rate)
#         else:
#             return 0.0
#
#     def days_used(self):
#         diff = datetime.date.today().year - self.purchase_date.year
#         return diff
#
#     def dispose(self):
#         self.is_disposed = True
#         self.save()
#
#     def dispose_asset(self):
#         return reverse(
#             'update-motor-vehicle',
#             kwargs={
#                 'pk': self.asset_id,
#                 'slug': self.slug
#             }
#         )
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.description)
#         super().save(*args, **kwargs)
#
#
# class Land(BaseAsset):
#     area = models.DecimalField(max_digits=10, decimal_places=2)
#     land_type = models.CharField(max_length=50)
#     title_deed_number = models.CharField(max_length=50, unique=True)
#     title_deed = models.FileField(upload_to='title deeds/')
#     registered_owner = models.CharField(max_length=255)
#
#     class Meta:
#         verbose_name_plural = 'Land'
#
#
# class Building(BaseAsset):
#     address = models.CharField(max_length=255)
#     construction_date = models.DateField()
#     floor_area = models.DecimalField(max_digits=10, decimal_places=2)
#     building_type = models.CharField(max_length=50)
#     number_of_floors = models.PositiveIntegerField()
#
#     class Meta:
#         verbose_name_plural = 'Buildings'
#
#
# class MotorVehicle(BaseAsset):
#     duty = models.DecimalField(default=0, decimal_places=2, max_digits=80)
#     freight = models.DecimalField(default=0, decimal_places=2, max_digits=25)
#     registration_number = models.CharField(max_length=20)
#     engine_number = models.CharField(max_length=50)
#     manufacturer = models.CharField(max_length=255)
#     model = models.CharField(max_length=255)
#     year = models.PositiveIntegerField()
#
#     class Meta:
#         verbose_name_plural = 'Motor Vehicles'
#
#
# class Machinery(BaseAsset):
#     serial_number = models.CharField(max_length=50)
#     manufacturer = models.CharField(max_length=255)
#     model = models.CharField(max_length=255)
#     capacity = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name_plural = 'Machinery'
#
#
# class Furniture(BaseAsset):
#     asset_tag = models.CharField(max_length=100, unique=True)
#     material = models.CharField(max_length=50)
#     condition = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name_plural = 'Furniture'
#
#
# class Equipment(BaseAsset):
#     serial_number = models.CharField(max_length=50, unique=True)
#     manufacturer = models.CharField(max_length=255)
#     asset_tag = models.CharField(max_length=100, blank=True)
#     model = models.CharField(max_length=255)
#     capacity = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name_plural = 'Equipment'
#
#     def __str__(self):
#         return self.name
#
#
# class Fixture(BaseAsset):
#     asset_tag = models.CharField(max_length=100)
#     location = models.ForeignKey(Room, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name_plural = 'Fixtures'
#
#
# class AssetDisposal(models.Model):
#     asset = models.OneToOneField(BaseAsset, on_delete=models.CASCADE)
#     disposal_date = models.DateField()
#     disposal_price = models.DecimalField(max_digits=10, decimal_places=2)
#     reason = models.CharField(max_length=255)
#     attachment1 = models.FileField(upload_to='disposals/', blank=True)
#     attachment2 = models.FileField(upload_to='disposals/', blank=True)
#     approved = models.BooleanField(default=False)
#     approved_date = models.DateTimeField(blank=True)
#     approvedBy = models.CharField(max_length=250, blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     def approve_disposal(self, approvedBy):
#         self.approved = True
#         self.approved_date = datetime.datetime.now()
#         self.approvedBy = approvedBy
#         self.asset.is_disposed = True
#         self.save()
#
#     class Meta:
#         verbose_name_plural = 'Asset Disposals'
#
#
# class AssetRepair(models.Model):
#     asset = models.ForeignKey(BaseAsset, on_delete=models.CASCADE)
#     repair_date = models.DateField()
#     repair_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     status = models.CharField(max_length=250, default='Pending Approval')
#     repair_quote = models.FileField(upload_to='repairs/', blank=True)
#     approved = models.BooleanField(default=False)
#     approved_date = models.DateTimeField(blank=True)
#     approvedBy = models.CharField(max_length=250, blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name_plural = 'Asset Repairs'
#
#     def approve_repair(self, approvedBy):
#         self.approved = True
#         self.approved_date = datetime.datetime.now()
#         self.approvedBy = approvedBy
#         self.save()
#
#
# class DepreciationEntry(models.Model):
#     asset = models.ForeignKey(BaseAsset, on_delete=models.CASCADE)
#     depreciation_date = models.DateField()
#     depreciation_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name_plural = 'Depreciation Entries'
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.asset.accumulated_depreciation += self.depreciation_amount
#         self.asset.last_depreciation_date = datetime.date.today()
#         self.asset.save()
#
#
# class AssetTransfer(models.Model):
#     transfer_id = models.BigAutoField(unique=True, primary_key=True)
#     asset = models.ForeignKey(BaseAsset, on_delete=models.CASCADE, related_name='transfers')
#     transfer_to = models.CharField(max_length=100)
#     transfer_from = models.CharField(max_length=100)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name_plural = 'Asset Transfers'
#
#     def __str__(self):
#         return self.asset.name

#
# class MotorVehicleDetail(models.Model):
#     mvd_id = models.BigAutoField(primary_key=True, unique=True)
#     asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='vehicle_details')
#     engine_number = models.CharField(max_length=80, unique=True)
#     chassis_number = models.CharField(max_length=80, unique=True)
#     duty = models.DecimalField(default=0, decimal_places=2, max_digits=80)
#     freight = models.DecimalField(default=0, decimal_places=2, max_digits=25)
#     reg_number = models.CharField(max_length=10, unique=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = "Motor Vehicle"
#
#     def __str__(self):
#         return self.asset.name
#
#     def edit_vehicle(self):
#         return reverse(
#             'update-motor-vehicle',
#             kwargs={
#                 'pk': self.mvd_id,
#                 'reg_number': self.reg_number
#             }
#         )
#
#     @property
#     def total_cost(self):
#         return self.asset.cost + self.freight + self.duty
#
#     @property
#     def total_depreciation(self):
#         value = self.asset.cost * self.asset.days_used() * Decimal(0.2)
#         return round(value, 2)
#
#     @property
#     def current_value(self):
#         value = self.total_cost - self.total_depreciation
#         if value > 0:
#             return round(value, 2)
#         else:
#             return '0.00'
#
#
# class FixtureAndFittingDetail(models.Model):
#     ffd_id = models.BigAutoField(primary_key=True)
#     asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='fixture_details')
#     asset_tag = models.CharField(max_length=100)
#     room = models.CharField(max_length=255, default="KITCHEN")
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = "Fixture and Fitting"
#
#     def __str__(self):
#         return self.asset.name
#
#     def edit_fixture_fitting(self):
#         return reverse(
#             'update-fixture-fitting',
#             kwargs={
#                 'pk': self.ffd_id,
#                 'asset_tag': self.asset_tag
#             }
#         )
#
#     @property
#     def total_depreciation(self):
#         value = self.asset.cost * self.asset.days_used() * Decimal(0.1)
#         return round(value, 2)
#
#     @property
#     def current_value(self):
#         value = self.asset.cost - self.total_depreciation
#         if value > 0:
#             return value
#         else:
#             return '0.00'
#
#
# class OfficeEquipmentDetail(models.Model):
#     oed_id = models.BigAutoField(primary_key=True, unique=True)
#     asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='office_details')
#     asset_tag = models.CharField(max_length=100, unique=True)
#     room = models.CharField(max_length=255, default="Workshop")
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = "Office Equipment"
#
#     def __str__(self):
#         return self.asset.name
#
#     def edit_office_equipment(self):
#         return reverse(
#             'update-office-equipment',
#             kwargs={
#                 'pk': self.oed_id,
#                 'asset_tag': self.asset_tag
#             }
#         )
#
#     @property
#     def total_depreciation(self):
#         value = self.asset.cost * self.asset.days_used() * Decimal(0.1)
#         return round(value, 2)
#
#     @property
#     def current_value(self):
#         value = self.asset.cost - self.total_depreciation
#         if value > 0:
#             return value
#         else:
#             return '0.00'
#
#
# class DataCenterDetail(models.Model):
#     dcd_id = models.BigAutoField(primary_key=True)
#     serial_number = models.CharField(max_length=100, unique=True)
#     warranty_end = models.DateField(blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = "Datacenter Equipment"
#
#     def __str__(self):
#         return self.asset.name
#
#     @property
#     def is_warranty_active(self):
#         return self.warranty_end > datetime.date.today()
#
#     def edit_datacenter_equipment(self):
#         return reverse(
#             'update-datacenter-equip',
#             kwargs={
#                 'pk': self.dcd_id,
#                 'serial_number': self.serial_number
#             }
#         )
#
#     @property
#     def total_depreciation(self):
#         value = self.asset.cost * self.asset.days_used() * Decimal(0.1)
#         return round(value, 2)
#
#     @property
#     def current_value(self):
#         value = self.asset.cost - self.total_depreciation
#         if value > 0:
#             return value
#         else:
#             return '0.00'
#
#     @property
#     def warranty_days(self):
#         diff = self.warranty_end - datetime.date.today()
#         return diff.days
#
#
# class ComputerEquipmentDetail(models.Model):
#     ced_id = models.BigAutoField(primary_key=True, unique=True)
#     asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='computer_details')
#     serial_number = models.CharField(max_length=100, unique=True)
#     warranty_end = models.DateField(blank=True)
#     room = models.CharField(max_length=255, default='SOFTWARE')
#     created_date = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = "Computer Equipment"
#
#     def __str__(self):
#         return self.asset.name
#
#     def is_warranty_active(self):
#         return self.warranty_end > datetime.date.today()
#
# def edit_computer_equipment(self):
#     return reverse(
#         'update-computer-equip',
#         kwargs={
#             'pk': self.ced_id,
#             'serial_number': self.serial_number
#         }
#     )
#
#     @property
#     def warranty_days(self):
#         diff = self.warranty_end - datetime.date.today()
#         return diff.days
#
#     @property
#     def total_depreciation(self):
#         value = self.asset.cost * self.asset.days_used() * Decimal(0.1)
#         return round(value, 2)
#
#     @property
#     def current_value(self):
#         value = self.asset.cost - self.total_depreciation
#         if value > 0:
#             return value
#         else:
#             return '0.00'
