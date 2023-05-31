from django import forms
from django.core.exceptions import ValidationError
from users.models import User
from betterforms.multiform import MultiModelForm
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime

from .models import (
    Room, Department, Vendor, BaseAsset, Land, Building, MotorVehicle,
    Machinery, Furniture, Equipment, Fixture, AssetDisposal, AssetRepair,
    DepreciationEntry, AssetTransfer
)

CONDITIONS = (
    ('NEW', 'NEW'),
    ('REFURB', 'REFURB'),
    ('USED', 'USED')
)

DEPRECIATION_METHODS = [
    ('SL', 'Straight-Line'),
    ('RB', 'Reducing Balance'),
    ('UP', 'Units of Production'),
]

REPAIR_STATUS = [
    ('IN PROGRESS', 'IN PROGRES'
                    'S'),
    ('COMPLETED', 'COMPLETED'),
    ('PENDING', 'PENDING')
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


class LandForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_value = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    area = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    land_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    title_deed_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    registered_owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = Land
        fields = ['name', 'useful_life', 'purchase_value', 'purchase_date',
                  'depreciation_rate', 'depreciation_method', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'area', 'land_type',
                  'title_deed_number', 'title_deed', 'registered_owner']


class BuildingForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_value = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    depreciation_rate = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    number_of_floors = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    floor_area = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    building_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    registered_owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    depreciation_method = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=DEPRECIATION_METHODS))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    construction_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = Building
        fields = ['name', 'useful_life', 'purchase_value', 'purchase_date',
                  'depreciation_rate', 'depreciation_method', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'address', 'construction_date',
                  'floor_area', 'building_type', 'number_of_floors']


class MotorVehicleForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_value = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    depreciation_rate = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    duty = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    registration_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    engine_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    freight = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    year = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    model = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    depreciation_method = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=DEPRECIATION_METHODS))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = MotorVehicle
        fields = ['name', 'useful_life', 'purchase_value', 'purchase_date',
                  'depreciation_rate', 'depreciation_method', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'duty', 'freight',
                  'registration_number', 'engine_number', 'manufacturer', 'model', 'year']


class MachineryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_value = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    depreciation_rate = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    model = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    capacity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    depreciation_method = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=DEPRECIATION_METHODS))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = Machinery
        fields = ['name', 'useful_life', 'purchase_value', 'purchase_date',
                  'depreciation_rate', 'depreciation_method', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'serial_number',
                  'manufacturer', 'model', 'capacity']


class FurnitureForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_value = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    depreciation_rate = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    asset_tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    material = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    condition = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    depreciation_method = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=DEPRECIATION_METHODS))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = Furniture
        fields = ['name', 'useful_life', 'purchase_value', 'purchase_date',
                  'depreciation_rate', 'depreciation_method', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'asset_tag',
                  'material', 'condition']


class EquipmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_value = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    depreciation_rate = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    asset_tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    capacity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    model = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    depreciation_method = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=DEPRECIATION_METHODS))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = Equipment
        fields = ['name', 'useful_life', 'purchase_value', 'purchase_date',
                  'depreciation_rate', 'depreciation_method', 'last_depreciation_date',
                  'accumulated_depreciation', 'is_disposed', 'serial_number',
                  'manufacturer', 'asset_tag', 'model', 'capacity']


class FixtureForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_value = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    useful_life = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    depreciation_rate = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    asset_tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    location = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                      queryset=Room.objects.all())
    depreciation_method = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', }, choices=DEPRECIATION_METHODS))
    purchase_date = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = Fixture
        fields = ['name', 'useful_life', 'purchase_value', 'purchase_date', 'depreciation_rate', 'depreciation_method',
                  'asset_tag', 'location']


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


class RepairForm(forms.ModelForm):
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    repair_date = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    status = forms.CharField(widget=forms.Select(attrs=({'class': 'form-control', }), choices=REPAIR_STATUS))
    asset = forms.CharField(required=False)

    class Meta:
        model = AssetRepair
        fields = ['repair_date', 'repair_cost', 'description', 'status', 'repair_quote']


class DisposalForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    asset = forms.CharField(required=False)
    disposal_date = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))

    class Meta:
        model = AssetDisposal
        fields = ['disposal_date', 'disposal_price', 'reason', 'attachment1', 'attachment2']
