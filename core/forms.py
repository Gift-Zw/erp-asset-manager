from django import forms
from django.core.exceptions import ValidationError
from users.models import User
from betterforms.multiform import MultiModelForm
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime

from .models import (
    Room, Department, Vendor, BaseAsset, Land, Building, MotorVehicle,
    Machinery, Furniture, Equipment, Fixture, AssetDisposal, AssetRepair,
    DepreciationEntry, AssetTransfer, AssetClassProperties
)

CONDITIONS = (
    ('NEW', 'NEW'),
    ('REFURB', 'REFURB'),
    ('USED', 'USED')
)

ASSET_SOURCES = [
    ('PURCHASED', 'PURCHASED'),
    ('DONATED', 'DONATED'),
    ('FORFEITED', 'FORFEITED')
]

REPAIR_STATUS = [
    ('IN PROGRESS', 'IN PROGRESS'),
    ('COMPLETED', 'COMPLETED'),
    ('PENDING', 'PENDING')
]

DISPOSAL_TYPES = [
    ('Auction', 'Auction'),
    ('Sale', 'Sale'),
    ('Trade In', 'Trade In')
]


def validate_date_not_in_future(value):
    if value > localtime().date():
        raise ValidationError("Date cannot be in the future")


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'is_deleted']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'is_deleted']


class DisposeAssetForm(forms.ModelForm):
    disposal_price = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    reason = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows':3 }))
    disposal_type = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=DISPOSAL_TYPES))
    disposal_date = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    attachment1 = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    attachment2 = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = AssetDisposal
        fields = ['disposal_type', 'disposal_date', 'disposal_price', 'reason', 'attachment1', 'attachment2']


class RepairAssetForm(forms.ModelForm):
    repair_cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    status = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=REPAIR_STATUS))
    repair_date = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    repair_quote = forms.FileField(required=False,
                                   widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = AssetRepair
        fields = ['repair_cost', 'description', 'status', 'repair_date', 'repair_quote']


class TransferAssetForm(forms.ModelForm):
    transfer_to = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    transfer_from = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    remarks = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows':3 }))
    transfer_date = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = AssetTransfer
        fields = ['transfer_date', 'transfer_to', 'transfer_from', 'remarks']


class AssetRevaluationForm(forms.Form):
    percentage = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    remarks = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))


class LandForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    area = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    land_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    source = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=ASSET_SOURCES))
    title_deed_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    registered_owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    asset_class = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                         queryset=AssetClassProperties.objects.filter().order_by('name'),
                                         empty_label='', required=True,
                                         )

    class Meta:
        model = Land
        fields = ['name', 'cost', 'purchase_date',
                  'source', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'area', 'land_type',
                  'title_deed_number', 'registered_owner', 'asset_class']


class BuildingForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    number_of_floors = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    floor_area = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    building_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    source = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=ASSET_SOURCES))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    construction_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    asset_class = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                         queryset=AssetClassProperties.objects.filter().order_by('name'),
                                         empty_label='', required=True,
                                         )

    class Meta:
        model = Building
        fields = ['name', 'useful_life', 'cost', 'purchase_date',
                  'source', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'address', 'construction_date',
                  'floor_area', 'building_type', 'number_of_floors', 'asset_class']


class MotorVehicleForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    duty = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    registration_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    engine_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    freight = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    year = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    model = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    source = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=ASSET_SOURCES))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    asset_class = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                         queryset=AssetClassProperties.objects.filter().order_by('name'),
                                         empty_label='', required=True,
                                         )

    class Meta:
        model = MotorVehicle
        fields = ['name', 'useful_life', 'cost', 'purchase_date',
                  'source',
                  'accumulated_depreciation', 'duty', 'freight',
                  'registration_number', 'engine_number', 'manufacturer', 'model', 'year', 'asset_class']


class MachineryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    model = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    capacity = forms.CharField(empty_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', }))
    source = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=ASSET_SOURCES))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    asset_class = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                         queryset=AssetClassProperties.objects.filter().order_by('name'),
                                         empty_label='', required=True,
                                         )

    class Meta:
        model = Machinery
        fields = ['name', 'useful_life', 'cost', 'purchase_date',
                  'source', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'serial_number',
                  'manufacturer', 'model', 'capacity', 'asset_class']


class FurnitureForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    asset_tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    material = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    condition = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    source = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=ASSET_SOURCES))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    asset_class = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                         queryset=AssetClassProperties.objects.filter().order_by('name'),
                                         empty_label='', required=True,
                                         )

    class Meta:
        model = Furniture
        fields = ['name', 'useful_life', 'cost', 'purchase_date',
                  'source', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'asset_tag',
                  'material', 'condition', 'asset_class']


class EquipmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    asset_tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    model = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    source = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=ASSET_SOURCES))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    asset_class = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                         queryset=AssetClassProperties.objects.filter().order_by('name'),
                                         empty_label='', required=True,
                                         )

    class Meta:
        model = Equipment
        fields = ['name', 'useful_life', 'cost', 'purchase_date', 'asset_class',
                  'source',
                  'accumulated_depreciation', 'is_disposed', 'serial_number',
                  'manufacturer', 'asset_tag', 'model', ]


class FixtureForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    asset_tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    location = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                      queryset=Room.objects.all())
    source = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=ASSET_SOURCES))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    asset_class = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                         queryset=AssetClassProperties.objects.filter().order_by('name'),
                                         empty_label='', required=True,
                                         )

    class Meta:
        model = Fixture
        fields = ['name', 'useful_life', 'cost', 'purchase_date', 'source',
                  'asset_tag', 'location', 'asset_class']


class VendorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', }))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), )
    address_line = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))

    class Meta:
        model = Vendor
        fields = ['name', 'email', 'phone', 'address_line', 'city', 'country']


class TransferForm(forms.ModelForm):
    asset = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    transfer_to = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    transfer_from = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    date_transferred = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', }))

    class Meta:
        model = AssetTransfer
        fields = ['asset', 'transfer_to', 'transfer_from', 'date_transferred', 'remarks', ]
