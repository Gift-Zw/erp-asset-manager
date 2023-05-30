from django import forms
from django.core.exceptions import ValidationError
from core import models
from users.models import User
from betterforms.multiform import MultiModelForm

CURRENCIES = (
    ('USD', 'USD'),
    ('ZWL', 'ZWL'),
    ('RAND', 'RAND')
)

CONDITIONS = (
    ('NEW', 'NEW'),
    ('REFURB', 'REFURB'),
    ('USED', 'USED')
)

ROOMS = (
    ('SOFTWARE', 'SOFTWARE'),
    ('WORKSHOP', 'WORKSHOP'),
    ('SALES', 'SALES'),
    ('DATACENTER', 'DATACENTER'),
    ('KITCHEN', 'KITCHEN'),
    ('BOARDROOM', 'BOARDROOM'),
    ('KITCHEN', 'KITCHEN'),
    ('RECEPTION', 'RECEPTION'),
    ('CEO OFFICE', 'CEO OFFICE'),
    ('SALES HOD', 'SALES HOD'),
    ('SOFTWARE HOD', 'SOFTWARE HOD'),
    ('SERVICES HOD', 'SERVICES HOD'),
    ('FINANCE HOD', 'FINANCE HOD'),
    ('ACCOUNTS OFFICE', 'ACCOUNTS OFFICE'),
    ('WORKSHOP ADMIN', 'WORKSHOP ADMIN'),
    ('GUEST TOILET', 'GUEST TOILET'),
    ('WORKSHOP TOILET', 'WORKSHOP TOILET'),
    ('MALE TOILET', 'MALE TOILET'),
    ('FEMALE TOILET', 'FEMALE TOILET')
)

REPAIR_STATUS = [
    ('IN PROGRESS', 'IN PROGRES'
                    'S'),
    ('COMPLETED', 'COMPLETED'),
    ('PENDING', 'PENDING')
]

from django.core.exceptions import ValidationError
from django.utils.timezone import localtime


def validate_date_not_in_future(value):
    if value > localtime().date():
        raise ValidationError("Date cannot be in the future")


class CreateAssetForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    purchase_value = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    grv_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    condition = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', }, choices=CONDITIONS))
    date_purchased = forms.DateField(validators=[validate_date_not_in_future], widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    vendor = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                    queryset=models.Vendor.objects.all())

    assignee = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                      queryset=models.User.objects.filter(is_staff=True).order_by('first_name'),
                                      empty_label='Unassigned', required=False,
                                      initial='Unassigned')

    class Meta:
        model = models.Asset
        fields = [
            'name', 'purchase_value', 'grv_number', 'date_purchased', 'vendor', 'assignee'
        ]


class CreateVendorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', }))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), )
    address_line = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))

    class Meta:
        model = models.Vendor
        fields = ['name', 'email', 'phone', 'address_line', 'city', 'country']


class MotorVehicleDetailForm(forms.ModelForm):
    engine_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    chassis_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    reg_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    freight = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    duty = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    asset = forms.CharField(required=False)

    class Meta:
        model = models.MotorVehicleDetail
        fields = ['engine_number', 'chassis_number', 'reg_number', 'freight', 'duty', 'asset']


class FixtureAndFittingDetailForm(forms.ModelForm):
    asset_tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    room = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', }, choices=ROOMS))
    asset = forms.CharField(required=False)

    class Meta:
        model = models.FixtureAndFittingDetail
        fields = ['asset_tag', 'room', 'asset']


class OfficeEquipmentDetailForm(forms.ModelForm):
    asset_tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    room = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', }, choices=ROOMS))
    asset = forms.CharField(required=False)

    class Meta:
        model = models.OfficeEquipmentDetail
        fields = ['asset_tag', 'room', 'asset']


class DataCenterDetailForm(forms.ModelForm):
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    warranty_end = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    asset = forms.CharField(required=False)

    class Meta:
        model = models.DataCenterDetail
        fields = ['serial_number', 'warranty_end', 'asset']


class ComputerEquipmentDetailForm(forms.ModelForm):
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    warranty_end = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    room = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', }, choices=ROOMS))
    asset = forms.CharField(required=False)

    class Meta:
        model = models.ComputerEquipmentDetail
        fields = ['serial_number', 'warranty_end', 'room', 'asset']


class TransferForm(forms.ModelForm):
    asset = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    transfer_to = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    transfer_from = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    date_transferred = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', }))

    class Meta:
        model = models.Transfer
        fields = ['asset', 'transfer_to', 'transfer_from', 'date_transferred', 'remarks', ]


class CreateRepairForm(forms.ModelForm):
    cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', }))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    date = forms.DateField(widget=forms.TextInput(attrs=(
        {'class': "form-control", 'id': "example-date", 'type': "date", 'name': "date"})))
    status = forms.CharField(widget=forms.Select(attrs=({'class': 'form-control', }), choices=REPAIR_STATUS))
    asset = forms.CharField(required=False)

    class Meta:
        model = models.Repair
        fields = ['cost', 'remarks', 'date', 'status']


class CreateDisposalForm(forms.ModelForm):
    remarks = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    asset = forms.CharField(required=False)

    class Meta:
        model = models.Disposal
        fields = ['remarks']


class CreateMotorVehicleForm(MultiModelForm):
    form_classes = {
        'vehicle': MotorVehicleDetailForm,
        'asset': CreateAssetForm
    }


class CreateOfficeEquipmentForm(MultiModelForm):
    form_classes = {
        'asset': CreateAssetForm,
        'office': OfficeEquipmentDetailForm
    }


class CreateFixtureAndFittingsForm(MultiModelForm):
    form_classes = {
        'asset': CreateAssetForm,
        'fitting': FixtureAndFittingDetailForm
    }


class CreateDataCenterEquipForm(MultiModelForm):
    form_classes = {
        'asset': CreateAssetForm,
        'datacenter': DataCenterDetailForm
    }


class CreateComputerEquipForm(MultiModelForm):
    form_classes = {
        'asset': CreateAssetForm,
        'computer': ComputerEquipmentDetailForm
    }
