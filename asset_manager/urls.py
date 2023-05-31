"""asset_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from core.views import index, MotorVehiclesView, FixtureAndFittingsView, OfficeEquipUpdateView, \
#     MyRepairsView, TransferView, logs_view, OfficeEquipView, MotorVehicleUpdateView, \
#     DisposedAssetsView, VendorView, VendorUploadView, MotorVehicleUploadView, OfficeEquipUploadView, \
#     FixtureAndFittingsUploadView, ComputerUploadView, DataCenterUploadView, ComputerEquipView, DataCenterView, \
#     VendorUpdateView, FixtureAndFittingUpdateView, ComputerEquipmentUpdateView, DataCenterUpdateView, \
#     DisposalView, AllRepairsView, \
#     RepairUploadView, RepairUpdateView, users_view, MyAssetsView, logout_view, delete_vendor
#
# from core.reports import comp_equip_csv, datacenter_csv, office_equip_csv, fixture_fitting_csv, motor_vehicles_csv, \
#     vendor_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', index, name="home"),
    # path('logout', logout_view, name='logOut'),
    # path('my-assets', MyAssetsView.as_view(), name="my-assets"),
    # path('motor-vehicles', MotorVehiclesView.as_view(), name="motor-vehicles"),
    # path('fixture-fittings', FixtureAndFittingsView.as_view(), name="fixture-fittings"),
    # path('office-equipment', OfficeEquipView.as_view(), name="office-equipment"),
    # path('data-center', DataCenterView.as_view(), name="data-center"),
    # path('computer-equipment', ComputerEquipView.as_view(), name="computer-equipment"),
    # path('repairs', MyRepairsView.as_view(), name="repairs"),
    # path('all-repairs', AllRepairsView.as_view(), name="all-repairs"),
    # path('users', users_view, name="users"),
    # path('create-repair/<int:asset_id>', RepairUploadView.as_view(), name="create-repair"),
    # path('update-repair/<int:pk>', RepairUpdateView.as_view(), name="update-repair"),
    # path('transfers', TransferView.as_view(), name="transfers"),
    # path('logs', logs_view, name="logs"),
    # path('disposed-assets', DisposedAssetsView.as_view(), name="disposed"),
    # path('vendors', VendorView.as_view(), name="vendors"),
    # path('create-vendor', VendorUploadView.as_view(), name="create-vendor"),
    # path('delete-vendor/<int:id>', delete_vendor, name="delete-vendor"),
    # path('update-vendor/<int:pk>-<str:name>', VendorUpdateView.as_view(), name="update-vendor"),
    # path('create-motor-vehicle', MotorVehicleUploadView.as_view(), name="create-motor-vehicle"),
    # path('update-motor-vehicle/<int:pk>-<str:reg_number>', MotorVehicleUpdateView.as_view(),
    #      name="update-motor-vehicle"),
    # path('create-office-equipment', OfficeEquipUploadView.as_view(), name="create-office-equipment"),
    # path('update-office-equipment/<int:pk>-<str:asset_tag>', OfficeEquipUpdateView.as_view(),
    #      name="update-office-equipment"),
    # path('create-fixture-fitting', FixtureAndFittingsUploadView.as_view(), name="create-fixture-fitting"),
    # path('update-fixture-fitting/<int:pk>-<str:asset_tag>', FixtureAndFittingUpdateView.as_view(),
    #      name="update-fixture-fitting"),
    # path('create-computer-equip', ComputerUploadView.as_view(), name="create-computer-equip"),
    # path('update-computer-equip/<int:pk>-<str:serial_number>', ComputerEquipmentUpdateView.as_view(),
    #      name="update-computer-equip"),
    # path('create-datacenter-equip', DataCenterUploadView.as_view(), name="create-datacenter-equip"),
    # path('update-datacenter-equip/<int:pk>-<str:serial_number>', DataCenterUpdateView.as_view(),
    #      name="update-datacenter-equip"),
    # path('dispose-asset/<int:asset_id>', DisposalView.as_view(), name="dispose-asset"),
    # path('computer-equip-csv', comp_equip_csv, name="computer-equip-csv"),
    # path('datacenter-equip-csv', datacenter_csv, name="datacenter-equip-csv"),
    # path('office-equip-csv', office_equip_csv, name="office-equip-csv"),
    # path('fixture-fittings-csv', fixture_fitting_csv, name="fixture-fittings-csv"),
    # path('motor-vehicles-csv', motor_vehicles_csv, name="motor-vehicles-csv"),
    # path('vendors-csv', vendor_csv, name="vendors-csv"),

]

# handler404 = 'core.views.error_404_view'
# handler500 = 'core.views.error_500_view'
