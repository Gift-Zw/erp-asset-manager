from decimal import Decimal

from .models import BaseAsset, Land, Building, Furniture, Fixture, Equipment, Machinery, MotorVehicle
from datetime import date


def revaluate_all_land(percentage, remarks, userName):
    assets = Land.objects.all()
    for land in assets:
        value = Decimal(percentage) * land.net_book_value / 100
        land.revalue_asset(value, remarks, userName)


def revaluate_all_buildings(percentage, remarks, userName):
    assets = Building.objects.all()
    for land in assets:
        value = Decimal(percentage) * land.net_book_value / 100
        land.revalue_asset(value, remarks, userName)


def revaluate_all_equipment(percentage, remarks, userName):
    assets = Equipment.objects.all()
    for land in assets:
        value = Decimal(percentage) * land.net_book_value / 100
        land.revalue_asset(value, remarks, userName)


def revaluate_all_furniture(percentage, remarks, userName):
    assets = Furniture.objects.all()
    for land in assets:
        value = Decimal(percentage) * land.net_book_value / 100
        land.revalue_asset(value, remarks, userName)


def revaluate_all_fixture(percentage, remarks, userName):
    assets = Fixture.objects.all()
    for land in assets:
        value = Decimal(percentage) * land.net_book_value / 100
        land.revalue_asset(value, remarks, userName)


def revaluate_all_machinery(percentage, remarks, userName):
    assets = Machinery.objects.all()
    for land in assets:
        value = Decimal(percentage) * land.net_book_value / 100
        land.revalue_asset(value, remarks, userName)


def revaluate_all_motor_vehicles(percentage, remarks, userName):
    assets = MotorVehicle.objects.all()
    for land in assets:
        value = Decimal(percentage) * land.net_book_value / 100
        land.revalue_asset(value, remarks, userName)
