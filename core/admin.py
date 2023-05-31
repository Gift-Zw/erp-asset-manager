from django.contrib import admin
from .models import (BaseAsset, Vendor, Room, Department, Land, Building, MotorVehicle, Machinery, Furniture, Equipment,
                     Fixture, AssetDisposal, AssetRepair, AssetTransfer, DepreciationEntry
                     )

# Register your models here.
admin.site.site_header = 'Kenac Asset Manager Admin'
admin.site.site_title = 'Kenac Asset Manager Admin'
admin.site.index_title = 'Kenac Asset Manager Administration'


class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_id', 'name', 'email', 'phone', 'address_line', 'city', 'country',]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_id', 'name', 'created_date', 'last_modified', 'is_deleted']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'name', 'created_date', 'last_modified', 'is_deleted']


class LandAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'registered_owner', 'purchase_value', 'purchase_date', 'useful_life',
                    'depreciation_rate', 'depreciation_method', 'last_depreciation_date', 'accumulated_depreciation',
                    'is_disposed']


class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'purchase_value', 'purchase_date', 'construction_date', 'address', 'building_type',
                    'floor_area', 'number_of_floors', 'useful_life', 'depreciation_rate', 'depreciation_method',
                    'last_depreciation_date', 'accumulated_depreciation', 'is_disposed']


class MotorVehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'purchase_value', 'purchase_date', 'duty', 'freight', 'registration_number',
                    'engine_number', 'manufacturer', 'model', 'year', 'useful_life', 'depreciation_rate',
                    'depreciation_method', 'last_depreciation_date', 'accumulated_depreciation', 'is_disposed']


class FurnitureAdmin(admin.ModelAdmin):
    list_display = ['name', 'asset_tag', 'material', 'condition', 'purchase_value', 'purchase_date', 'useful_life',
                    'depreciation_rate', 'depreciation_method', 'last_depreciation_date', 'accumulated_depreciation',
                    'is_disposed']


class MachineryAdmin(admin.ModelAdmin):
    list_display = ['name', 'purchase_value', 'serial_number', 'manufacturer', 'model', 'capacity', 'purchase_date',
                    'useful_life', 'depreciation_rate', 'depreciation_method', 'last_depreciation_date',
                    'accumulated_depreciation', 'is_disposed']


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'purchase_value', 'serial_number', 'manufacturer', 'model', 'asset_tag', 'purchase_date',
                    'useful_life', 'depreciation_rate', 'depreciation_method', 'last_depreciation_date',
                    'accumulated_depreciation', 'is_disposed']


class FixtureAdmin(admin.ModelAdmin):
    list_display = ['name', 'purchase_value', 'asset_tag', 'location', 'purchase_date', 'useful_life',
                    'depreciation_rate', 'depreciation_method', 'last_depreciation_date', 'accumulated_depreciation',
                    'is_disposed']


class TransferAdmin(admin.ModelAdmin):
    list_display = ['transfer_id', 'asset', 'transfer_to', 'transfer_from',
                    'created_date', 'last_modified']


class DisposalAdmin(admin.ModelAdmin):
    list_display = ['asset', 'disposal_date', 'disposal_price', 'reason', 'approved', 'approvedBy', 'approved_date',
                    'created_date', 'last_modified', ]


class RepairAdmin(admin.ModelAdmin):
    list_display = ['id', 'asset', 'repair_cost', 'repair_date', 'description', 'status', 'approved', 'approvedBy',
                    'created_date', 'last_modified', ]


class DepreciationAdmin(admin.ModelAdmin):
    list_display = ['asset', 'depreciation_date', 'depreciation_amount',
                    'created_date', 'last_modified']


admin.site.register(Vendor, VendorAdmin)
admin.site.register(MotorVehicle, MotorVehicleAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Machinery, MachineryAdmin)
admin.site.register(Furniture, FurnitureAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(AssetDisposal, DisposalAdmin)
admin.site.register(AssetRepair, RepairAdmin)
admin.site.register(DepreciationEntry, DepreciationAdmin)
admin.site.register(AssetTransfer, TransferAdmin)
admin.site.register(Room, RoomAdmin)
