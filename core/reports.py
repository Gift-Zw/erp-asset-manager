import csv
from datetime import date
from django.http import HttpResponse

from .models import ComputerEquipmentDetail, DataCenterDetail, OfficeEquipmentDetail, FixtureAndFittingDetail, \
    MotorVehicleDetail, Vendor


def vendor_csv(request):
    vendor_list = Vendor.objects.all()
    response = HttpResponse(content_type='text/csv')
    file_name = 'vendors-{0}.csv'.format(date.today())
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'Address Line', 'City', 'Country', 'Date Added'])
    vendors = vendor_list.values_list('name', 'email', 'phone', 'address_line', 'city', 'country', 'created_date')
    for vendor in vendors:
        writer.writerow(vendor)
    return response


def comp_equip_csv(request):
    comp_equip = ComputerEquipmentDetail.objects.filter(asset__is_disposed=False)
    response = HttpResponse(content_type='text/csv')
    file_name = 'computer-equipment-{0}.csv'.format(date.today())
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    writer = csv.writer(response)
    writer.writerow(
        ['Name', 'Serial Number', 'GRV Number', 'Warranty End Date', 'Room', 'Currency', 'Cost', 'Condition',
         'Date Purchased', 'Vendor', 'Vendor Email', 'Assignee First Name', 'Assignee Last Name',
         'Date Created',
         'Last Modified'])

    equip = comp_equip.values_list('asset__name', 'serial_number', 'asset__grv_number', 'warranty_end', 'room',
                                   'asset__currency',
                                   'asset__cost', 'asset__condition', 'asset__date_purchased',
                                   'asset__vendor__name', 'asset__vendor__email', 'asset__assignee__first_name',
                                   'asset__assignee__last_name',
                                   'asset__created_date', 'last_modified')
    for asset in equip:
        writer.writerow(asset)
    return response


def datacenter_csv(request):
    datacenter_equip = DataCenterDetail.objects.filter(asset__is_disposed=False)
    response = HttpResponse(content_type='text/csv')
    file_name = 'datacenter-equipment-{0}.csv'.format(date.today())
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    writer = csv.writer(response)
    writer.writerow(
        ['Name', 'Serial Number', 'GRV Number' 'Warranty End Date', 'Room', 'Currency', 'Cost', 'Condition',
         'Date Purchased', 'Vendor', 'Vendor Email', 'Assignee First Name', 'Assignee Last Name',
         'Date Created',
         'Last Modified'])

    equip = datacenter_equip.values_list('asset__name', 'serial_number', 'asset__grv_number', 'warranty_end', 'room',
                                         'asset__currency',
                                         'asset__cost', 'asset__condition', 'asset__date_purchased',
                                         'asset__vendor__name', 'asset__vendor__email', 'asset__assignee__first_name',
                                         'asset__assignee__last_name',
                                         'asset__created_date', 'last_modified')
    for asset in equip:
        writer.writerow(asset)
    return response


def office_equip_csv(request):
    office_equip = OfficeEquipmentDetail.objects.filter(asset__is_disposed=False)
    response = HttpResponse(content_type='text/csv')
    file_name = 'office-equipment-{0}.csv'.format(date.today())
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    writer = csv.writer(response)
    writer.writerow(['Name', 'Asset Tag', 'GRV NUmber', 'Room', 'Currency', 'Cost', 'Condition',
                     'Date Purchased', 'Vendor', 'Vendor Email', 'Assignee First Name', 'Assignee Last Name',
                     'Date Created',
                     'Last Modified'])

    equip = office_equip.values_list('asset__name', 'asset_tag', 'asset__grv_number', 'room', 'asset__currency',
                                     'asset__cost', 'asset__condition', 'asset__date_purchased',
                                     'asset__vendor__name', 'asset__vendor__email', 'asset__assignee__first_name',
                                     'asset__assignee__last_name',
                                     'asset__created_date', 'last_modified')
    for asset in equip:
        writer.writerow(asset)
    return response


def fixture_fitting_csv(request):
    fixture_fitting = FixtureAndFittingDetail.objects.filter(asset__is_disposed=False)
    response = HttpResponse(content_type='text/csv')
    file_name = 'fixtures-fittings-{0}.csv'.format(date.today())
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    writer = csv.writer(response)
    writer.writerow(['Name', 'Asset Tag', 'GRV Number', 'Room', 'Currency', 'Cost', 'Condition',
                     'Date Purchased', 'Vendor', 'Vendor Email', 'Assignee First Name', 'Assignee Last Name',
                     'Date Created',
                     'Last Modified'])

    equip = fixture_fitting.values_list('asset__name', 'asset_tag', 'asset__grv_number', 'room', 'asset__currency',
                                        'asset__cost', 'asset__condition', 'asset__date_purchased',
                                        'asset__vendor__name', 'asset__vendor__email', 'asset__assignee__first_name',
                                        'asset__assignee__last_name',
                                        'asset__created_date', 'last_modified')
    for asset in equip:
        writer.writerow(asset)
    return response


def motor_vehicles_csv(request):
    motor_vehicles = MotorVehicleDetail.objects.filter(asset__is_disposed=False)
    response = HttpResponse(content_type='text/csv')
    file_name = 'vendors-{0}.csv'.format(date.today())
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    writer = csv.writer(response)
    writer.writerow(
        ['Name', 'Registration Number', 'Engine Number', 'Chassis Number', 'GRV Number', 'Currency', 'Cost',
         'Condition',
         'Date Purchased', 'Vendor', 'Vendor Email', 'Assignee First Name', 'Assignee Last Name',
         'Date Created',
         'Last Modified'])

    vehicles = motor_vehicles.values_list('asset__name', 'reg_number', 'engine_number', 'chassis_number',
                                          'asset__grv_number',
                                          'asset__currency',
                                          'asset__cost', 'asset__condition', 'asset__date_purchased',
                                          'asset__vendor__name', 'asset__vendor__email', 'asset__assignee__first_name',
                                          'asset__assignee__last_name',
                                          'asset__created_date', 'last_modified')
    for vehicle in vehicles:
        writer.writerow(vehicle)
    return response
