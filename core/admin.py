from django.contrib import admin
from .models import (Asset, Vendor, MotorVehicleDetail,
                     FixtureAndFittingDetail, OfficeEquipmentDetail, DataCenterDetail,
                     ComputerEquipmentDetail, Transfer, Repair,
                     )

# Register your models here.
admin.site.site_header = 'Kenac Asset Manager Admin'
admin.site.site_title = 'Kenac Asset Manager Admin'
admin.site.index_title = 'Kenac Asset Manager Administration'


class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'purchase_value', 'is_disposed']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_id', 'name', 'email', 'phone', 'address_line', 'city', 'country', 'created_date',
                    'last_modified']



class MotorVehicleDetailAdmin(admin.ModelAdmin):
    list_display = ['mvd_id', 'asset', 'engine_number', 'chassis_number', 'freight', 'duty', 'reg_number', 'created_date', 'last_modified']


class FixtureAndFittingDetailAdmin(admin.ModelAdmin):
    list_display = ['ffd_id', 'asset', 'asset_tag', 'created_date', 'last_modified']


class OfficeEquipmentDetailAdmin(admin.ModelAdmin):
    list_display = ['oed_id', 'asset', 'asset_tag', 'created_date', 'last_modified']


class DataCenterDetailAdmin(admin.ModelAdmin):
    list_display = ['dcd_id', 'asset', 'serial_number', 'warranty_end', 'created_date', 'last_modified']


class ComputerEquipmentDetailAdmin(admin.ModelAdmin):
    list_display = ['ced_id', 'asset', 'serial_number', 'warranty_end', 'created_date', 'last_modified']


class TransferAdmin(admin.ModelAdmin):
    list_display = ['transfer_id', 'asset', 'transfer_to', 'transfer_from',
                    'created_date', 'last_modified']


class RepairAdmin(admin.ModelAdmin):
    list_display = ['repair_id', 'asset', 'cost', 'date', 'remarks', 'status', 'created_date', 'last_modified']


admin.site.register(Asset, AssetAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(MotorVehicleDetail, MotorVehicleDetailAdmin)
admin.site.register(OfficeEquipmentDetail, OfficeEquipmentDetailAdmin)
admin.site.register(DataCenterDetail, DataCenterDetailAdmin)
admin.site.register(ComputerEquipmentDetail, ComputerEquipmentDetailAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(Repair, RepairAdmin)
