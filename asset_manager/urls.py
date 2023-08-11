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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from core.views import index, AssetDisposalApprovalView
from core.views import (
    RoomCreateView, RoomUpdateView, RoomListView,
    DepartmentCreateView, DepartmentUpdateView, DepartmentListView,
    LandCreateView, LandUpdateView, LandListView, LandDisposalView, LandRevaluateAssetsView,
    BuildingCreateView, BuildingUpdateView, BuildingListView, BuildingDisposalView, BuildingRepairView, BuildingRevaluateAssetsView, BuildingTransferView,
    MotorVehicleCreateView, MotorVehicleUpdateView, MotorVehicleListView, MotorVehicleDisposalView, MotorVehicleRevaluateAssetsView, MotorVehicleTransferView,
    MotorVehicleRepairView,
    MachineryCreateView, MachineryUpdateView, MachineryListView, MachineryDisposalView, MachineryRepairView, MachineryRevaluateAssetsView, MachineryTransferView,
    FurnitureCreateView, FurnitureUpdateView, FurnitureListView, FurnitureDisposalView, FurnitureRepairView, FurnitureRevaluateAssetsView, FurnitureTransferView,
    EquipmentCreateView, EquipmentUpdateView, EquipmentListView, EquipmentDisposalView, EquipmentRepairView, EquipmentRevaluateAssetsView, EquipmentTransferView,
    FixtureCreateView, FixtureUpdateView, FixtureListView, FixtureDisposalView, FixtureRepairView, FixtureRevaluateAssetsView, FixtureTransferView,
    error_404_view, error_500_view, logout_view, PendingDisposalListView, ApprovedDisposalListView, AssetDisposalRejectionView, RejectedDisposalListView,
    ApprovedRepairListView, PendingRepairListView, RepairAssetApprovalView, UserListView, AssetClassesListView, RevaluationHistoryListView, PendingTransfersListView, ApprovedTransfersListView, TransferApprovalView, TransferRejectionView, RejectedTransfersListView, RejectedRepairListView, RepairAssetRejectionView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index, name="home"),

    # Room
    path('room/create/', RoomCreateView.as_view(), name='room-create'),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('room/', RoomListView.as_view(), name='room-list'),

    # Department
    path('department/create/', DepartmentCreateView.as_view(), name='department-create'),
    path('department/<int:pk>/update/', DepartmentUpdateView.as_view(), name='department-update'),
    path('department/', DepartmentListView.as_view(), name='department-list'),

    # Land
    path('land/create/', LandCreateView.as_view(), name='land-create'),
    path('land/<int:pk>/update/', LandUpdateView.as_view(), name='land-update'),
    path('land/', LandListView.as_view(), name='land-list'),
    path('land/<int:pk>/dispose/', LandDisposalView.as_view(), name='land-dispose'),
    path('land/revaluate/', LandRevaluateAssetsView.as_view(), name='land-revaluate'),

    # Building
    path('building/create/', BuildingCreateView.as_view(), name='building-create'),
    path('building/<int:pk>/update/', BuildingUpdateView.as_view(), name='building-update'),
    path('building/', BuildingListView.as_view(), name='building-list'),
    path('building/<int:pk>/dispose/', BuildingDisposalView.as_view(), name='building-dispose'),
    path('building/<int:pk>/repair/', BuildingRepairView.as_view(), name='building-repair'),
    path('building/revaluate/', BuildingRevaluateAssetsView.as_view(), name='building-revaluate'),
    path('building/<int:pk>/transfer/', BuildingTransferView.as_view(), name='building-transfer'),

    # MotorVehicle
    path('motorvehicle/create/', MotorVehicleCreateView.as_view(), name='motor-vehicle-create'),
    path('motorvehicle/<int:pk>/update/', MotorVehicleUpdateView.as_view(), name='motor-vehicle-update'),
    path('motorvehicle/', MotorVehicleListView.as_view(), name='motor-vehicle-list'),
    path('motorvehicle/<int:pk>/dispose/', MotorVehicleDisposalView.as_view(), name='motor-vehicle-dispose'),
    path('motorvehicle/<int:pk>/repair/', MotorVehicleRepairView.as_view(), name='motor-vehicle-repair'),
    path('motorvehicle/revaluate/', MotorVehicleRevaluateAssetsView.as_view(), name='motor-vehicle-revaluate'),
    path('motorvehicle/<int:pk>/transfer/', MotorVehicleTransferView.as_view(), name='motor-vehicle-transfer'),


    # Machinery
    path('machinery/create/', MachineryCreateView.as_view(), name='machinery-create'),
    path('machinery/<int:pk>/update/', MachineryUpdateView.as_view(), name='machinery-update'),
    path('machinery/', MachineryListView.as_view(), name='machinery-list'),
    path('machinery/<int:pk>/dispose/', MachineryDisposalView.as_view(), name='machinery-dispose'),
    path('machinery/<int:pk>/repair/', MachineryRepairView.as_view(), name='machinery-repair'),
    path('machinery/revaluate/', MachineryRevaluateAssetsView.as_view(), name='machinery-revaluate'),
    path('machinery/<int:pk>/transfer/', MachineryTransferView.as_view(), name='machinery-transfer'),

    # Furniture
    path('furniture/create/', FurnitureCreateView.as_view(), name='furniture-create'),
    path('furniture/<int:pk>/update/', FurnitureUpdateView.as_view(), name='furniture-update'),
    path('furniture/', FurnitureListView.as_view(), name='furniture-list'),
    path('furniture/<int:pk>/dispose/', FurnitureDisposalView.as_view(), name='furniture-dispose'),
    path('furniture/<int:pk>/repair/', FurnitureRepairView.as_view(), name='furniture-repair'),
    path('furniture/revaluate/', FurnitureRevaluateAssetsView.as_view(), name='furniture-revaluate'),
    path('furniture/<int:pk>/transfer/', FurnitureTransferView.as_view(), name='furniture-transfer'),

    # Fixture
    path('fixture/create/', FixtureCreateView.as_view(), name='fixture-create'),
    path('fixture/<int:pk>/update/', FixtureUpdateView.as_view(), name='fixture-update'),
    path('fixture/', FixtureListView.as_view(), name='fixture-list'),
    path('fixture/<int:pk>/dispose/', FixtureDisposalView.as_view(), name='fixture-dispose'),
    path('fixture/<int:pk>/repair/', FixtureRepairView.as_view(), name='fixture-repair'),
    path('fixture/revaluate/', FixtureCreateView.as_view(), name='fixture-revaluate'),
    path('fixture/<int:pk>/transfer/', FixtureTransferView.as_view(), name='fixture-transfer'),

    # Equipment
    path('equipment/create/', EquipmentCreateView.as_view(), name='equipment-create'),
    path('equipment/<int:pk>/update/', EquipmentUpdateView.as_view(), name='equipment-update'),
    path('equipment/', EquipmentListView.as_view(), name='equipment-list'),
    path('equipment/<int:pk>/dispose/', EquipmentDisposalView.as_view(), name='equipment-dispose'),
    path('equipment/<int:pk>/repair/', EquipmentRepairView.as_view(), name='equipment-repair'),
    path('equipment/revaluate/', EquipmentRevaluateAssetsView   .as_view(), name='equipment-revaluate'),
    path('equipment/<int:pk>/transfer/', EquipmentTransferView.as_view(), name='equipment-transfer'),


    # Error views
    path('404/', error_404_view, name='error-404'),
    path('500/', error_500_view, name='error-500'),

    # Disposal Views
    path('disposed/approved/', ApprovedDisposalListView.as_view(), name='approved-disposal'),
    path('disposed/pending/', PendingDisposalListView.as_view(), name='pending-disposal'),
    path('disposed/rejected/', RejectedDisposalListView.as_view(), name='rejected-disposal'),
    path('disposal/<int:pk>/approve/', AssetDisposalApprovalView.as_view(), name='asset-disposal-approve'),
    path('disposal/<int:pk>/reject/', AssetDisposalRejectionView.as_view(), name='asset-disposal-reject'),

    # Repair Views
    path('repairs/approved/', ApprovedRepairListView.as_view(), name='repair-approved'),
    path('repairs/pending/', PendingRepairListView.as_view(), name='repair-pending'),
    path('repairs/rejected/', RejectedRepairListView.as_view(), name='repair-rejected'),
    path('repairs/<int:pk>/approve/', RepairAssetApprovalView.as_view(), name='asset-repair-approve'),
    path('repairs/<int:pk>/reject/', RepairAssetRejectionView.as_view(), name='asset-repair-reject'),

    # Transfers
    path('transfers/approved/', ApprovedTransfersListView.as_view(), name='transfer-approved'),
    path('transfers/pending/', PendingTransfersListView.as_view(), name='transfer-pending'),
    path('transfers/rejected/', RejectedTransfersListView.as_view(), name='transfer-rejected'),
    path('transfers/<int:pk>/approve/', TransferApprovalView.as_view(), name='approve-transfer'),
    path('transfers/<int:pk>/reject/', TransferRejectionView.as_view(), name='reject-transfer'),


    # User
    path('users', UserListView.as_view(), name='user-list'),
    path('logout', logout_view, name='logOut'),

    # Depreciation
    path('asset-classes/', AssetClassesListView.as_view(), name='asset-classes'),

    path('revaluation/', RevaluationHistoryListView.as_view(), name="revaluation-history")

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# handler404 = 'core.views.error_404_view'
# handler500 = 'core.views.error_500_view'
