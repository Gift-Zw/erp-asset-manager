import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.generic import CreateView, ListView, UpdateView
from core import models, forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q, Sum
from django.contrib import messages
from core import revaluation

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from .models import Room, Department, Land, Building, MotorVehicle, Machinery, Furniture, Equipment, Fixture, \
    AssetClassProperties, \
    AssetDisposal, AssetRepair, BaseAsset, AssetRevaluationRecord, AssetTransfer
from .forms import RoomForm, DepartmentForm, LandForm, BuildingForm, FixtureForm, MotorVehicleForm, MachineryForm, \
    FurnitureForm, \
    EquipmentForm, DisposeAssetForm, RepairAssetForm, AssetRevaluationForm, TransferAssetForm
from users.models import User


def calculate_acc_dep(model: BaseAsset):
    assets = model.objects.filter(is_disposed=False)
    acc_dep = Decimal()
    for asset in assets:
        acc_dep = asset.get_accumulated_depreciation + acc_dep

    return acc_dep


def calculate_total_cost(model: BaseAsset):
    cost = model.objects.filter(is_disposed=False).aggregate(total=Sum('cost')).get('total', 0)
    return cost or 0


def calculate_total_repair(model: BaseAsset):
    content_type = ContentType.objects.get_for_model(model)
    cost = AssetRepair.objects.filter(content_type=content_type, approved=True).aggregate(total=Sum('repair_cost')).get(
        'total', 0)
    return cost or 0


@login_required
def index(request):
    building_acc_dep = calculate_acc_dep(Building)
    nbv_buildings = calculate_total_cost(Building) - building_acc_dep
    nbv_land = calculate_total_cost(Land)
    furniture_acc_dep = calculate_acc_dep(Furniture)
    nbv_furniture = calculate_total_cost(Furniture) - furniture_acc_dep
    fixture_acc_dep = calculate_acc_dep(Fixture)
    nbv_fixture = calculate_total_cost(Fixture) - fixture_acc_dep
    machinery_acc_dep = calculate_acc_dep(Machinery)
    nbv_machinery = calculate_total_cost(Machinery) - machinery_acc_dep
    motor_vehicles_acc_dep = calculate_acc_dep(MotorVehicle)
    nbv_motor_vehicles = calculate_total_cost(MotorVehicle) - motor_vehicles_acc_dep
    equipment_acc_dep = calculate_acc_dep(Equipment)
    nbv_equipment = calculate_total_cost(Equipment) - equipment_acc_dep
    total_acc_dep = building_acc_dep + furniture_acc_dep + fixture_acc_dep + machinery_acc_dep + motor_vehicles_acc_dep + equipment_acc_dep
    total_nbv = nbv_equipment + nbv_motor_vehicles + nbv_machinery + nbv_land + nbv_fixture + nbv_buildings + nbv_furniture
    total_buildings = Building.objects.filter(is_disposed=False).count()
    total_land = Land.objects.filter(is_disposed=False).count()
    total_furniture = Furniture.objects.filter(is_disposed=False).count()
    total_fixture = Fixture.objects.filter(is_disposed=False).count()
    total_equipment = Equipment.objects.filter(is_disposed=False).count()
    total_machinery = Machinery.objects.filter(is_disposed=False).count()
    total_motor_vehicles = MotorVehicle.objects.filter(is_disposed=False).count()
    total_assets = total_motor_vehicles + total_machinery + total_equipment + total_land + total_fixture + total_furniture + total_buildings
    total_disposed = AssetDisposal.objects.all().count()
    total_disposed_approved = AssetDisposal.objects.filter(approved=True).count()
    total_repairs = AssetRepair.objects.all().count()
    repairs_pending_approval = AssetRepair.objects.filter(approved=False).count()
    inprogress_repairs = AssetRepair.objects.filter(status='IN PROGRESS').count()
    rejected_repairs = AssetRepair.objects.filter(is_rejected=True).count()
    total_transfers = AssetTransfer.objects.filter(is_approved=True).count()
    context = {
        'total_buildings': total_buildings,
        'total_land': total_land,
        'total_furniture': total_furniture,
        'total_fixture': total_fixture,
        'total_equipment': total_equipment,
        'total_machinery': total_machinery,
        'total_motor_vehicles': total_motor_vehicles,
        'total_disposed': total_disposed,
        'total_disposed_approved': total_disposed_approved,
        'total_repairs': total_repairs,
        'repairs_pending_approval': repairs_pending_approval,
        'revaluation_records': AssetRevaluationRecord.objects.all()[:5],
        'total_expense': AssetRepair.objects.filter(approved=True).aggregate(total=Sum('repair_cost')).get('total', 0),
        'inprogress_repairs': inprogress_repairs,
        'rejected_repairs': rejected_repairs,
        'total_assets': total_assets,
        'total_transfers': total_transfers,
        'total_nbv': total_nbv,
        'total_acc_dep': total_acc_dep,
    }
    return render(request, 'index.html', context=context)


# Base class for Create views
class BaseCreateView(CreateView):
    template_name = ''
    success_url = reverse_lazy('')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully added the asset to the system.')
        return response
    #
    # def form_invalid(self, form):
    #     print(form.errors)
    #     return HttpResponse(form.errors)


# Base class for Update views
class BaseUpdateView(UpdateView):
    template_name = ''
    success_url = reverse_lazy('')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully updated the asset.')
        return response


# Base class for List views
class BaseListView(ListView):
    template_name = ''
    context_object_name = ''


# Room
class RoomCreateView(BaseCreateView):
    model = Room
    form_class = RoomForm
    template_name = 'forms/add_room.html'
    success_url = reverse_lazy('room-list')


class RoomUpdateView(BaseUpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'forms/update_room.html'
    success_url = reverse_lazy('room-list')


class RoomListView(BaseListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'


# Department
class DepartmentCreateView(BaseCreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'forms/add_department.html'
    success_url = reverse_lazy('department-list')


class DepartmentUpdateView(BaseUpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'forms/update_department.html'
    success_url = reverse_lazy('department-list')


class DepartmentListView(BaseListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'


# Land
class LandCreateView(BaseCreateView):
    model = Land
    form_class = LandForm
    template_name = 'forms/add_land.html'
    success_url = reverse_lazy('land-list')


class LandUpdateView(BaseUpdateView):
    model = Land
    form_class = LandForm
    template_name = 'forms/update_land.html'
    success_url = reverse_lazy('land-list')

    def get_context_data(self, **kwargs):
        kwargs = super(LandUpdateView, self).get_context_data()
        asset = self.object
        content_type = ContentType.objects.get_for_model(asset)
        asset_id = asset.asset_id

        kwargs.update({
            'repairs': models.AssetRepair.objects.filter(object_id=asset_id, content_type=content_type),
            'revaluations': models.AssetRevaluationRecord.objects.filter(object_id=asset_id, content_type=content_type)
        })
        return kwargs


class LandListView(BaseListView):
    model = Land
    template_name = 'land_list.html'
    context_object_name = 'lands'
    queryset = Land.objects.filter(is_disposed=False, pending_disposal=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional variables to the context
        context['form'] = AssetRevaluationForm()
        context['total_value'] = calculate_total_cost(Land)
        return context


class LandDisposalView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Land, pk=pk)
        form = DisposeAssetForm()
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Land, pk=pk)
        form = DisposeAssetForm(request.POST, request.FILES)
        if form.is_valid():
            disposal_date = form.cleaned_data['disposal_date']
            disposal_price = form.cleaned_data['disposal_price']
            disposal_type = form.cleaned_data['disposal_type']
            reason = form.cleaned_data['reason']
            repair_quote = form.cleaned_data['repair_quote']
            asset.dispose_land(disposal_date, disposal_type, disposal_price, reason, repair_quote)
            return redirect('pending-disposal')
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})


class LandRevaluateAssetsView(View):
    def get(self, request):
        return redirect('land-list')

    def post(self, request):
        form = AssetRevaluationForm(request.POST)
        if form.is_valid():
            revaluation.revaluate_all_land(form.cleaned_data['percentage'], form.cleaned_data['remarks'],
                                           request.user.full_name)
            return redirect('land-list')
        else:
            return reverse_lazy('land-list')


class FixtureCreateView(BaseCreateView):
    model = Fixture
    form_class = FixtureForm
    template_name = 'forms/add_fixture.html'
    success_url = reverse_lazy('fixture-list')


class FixtureUpdateView(BaseUpdateView):
    model = Fixture
    form_class = FixtureForm
    template_name = 'forms/update_fixture.html'
    success_url = reverse_lazy('fixture-list')

    def get_context_data(self, **kwargs):
        kwargs = super(FixtureUpdateView, self).get_context_data()
        asset = self.object
        content_type = ContentType.objects.get_for_model(asset)
        asset_id = asset.asset_id

        kwargs.update({
            'repairs': models.AssetRepair.objects.filter(object_id=asset_id, content_type=content_type),
            'revaluations': models.AssetRevaluationRecord.objects.filter(object_id=asset_id, content_type=content_type)
        })
        return kwargs


class FixtureListView(BaseListView):
    model = Fixture
    template_name = 'fixture_list.html'
    context_object_name = 'fixtures'
    queryset = Fixture.objects.filter(is_disposed=False, pending_disposal=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional variables to the context
        context['form'] = AssetRevaluationForm()
        context['total_dep'] = calculate_acc_dep(Fixture)
        context['total_value'] = calculate_total_cost(Fixture)
        context['total_repair'] = calculate_total_repair(Fixture)
        return context


class FixtureDisposalView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Fixture, pk=pk)
        form = DisposeAssetForm()
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Fixture, pk=pk)
        form = DisposeAssetForm(request.POST, request.FILES)
        if form.is_valid():
            disposal_date = form.cleaned_data['disposal_date']
            disposal_price = form.cleaned_data['disposal_price']
            disposal_type = form.cleaned_data['disposal_type']
            reason = form.cleaned_data['reason']
            # attachment1 = form.cleaned_data['attachment1']
            # attachment2 = form.cleaned_data['attachment2']
            asset.dispose_fixture(disposal_date, disposal_type, disposal_price, reason)
            return redirect('pending-disposal')
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})


class FixtureRepairView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Fixture, pk=pk)
        form = RepairAssetForm()
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Fixture, pk=pk)
        form = RepairAssetForm(request.POST, request.FILES)
        if form.is_valid():
            repair_date = form.cleaned_data['repair_date']
            repair_cost = form.cleaned_data['repair_cost']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            repair_quote = form.cleaned_data['repair_quote']
            asset.repair_fixture(repair_date, repair_cost, description, status, repair_quote)
            return redirect('repair-pending')
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})


class FixtureRevaluateAssetsView(View):
    def get(self, request):
        return redirect('fixture-list')

    def post(self, request):
        form = AssetRevaluationForm(request.POST)
        if form.is_valid():
            revaluation.revaluate_all_fixture(form.cleaned_data['percentage'], form.cleaned_data['remarks'],
                                              request.user.full_name)
            return redirect('fixture-list')
        else:
            return reverse_lazy('fixture-list')


class FixtureTransferView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Fixture, pk=pk)
        form = TransferAssetForm()
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Fixture, pk=pk)
        form = TransferAssetForm(request.POST)
        if form.is_valid():
            transfer_date = form.cleaned_data['transfer_date']
            transfer_to = form.cleaned_data['transfer_to']
            transfer_from = form.cleaned_data['transfer_from']
            remarks = form.cleaned_data['remarks']
            asset.transfer_fixture(transfer_date, transfer_to, transfer_from, remarks)
            return redirect('transfer-pending')
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})


# Building
class BuildingCreateView(BaseCreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'forms/add_building.html'
    success_url = reverse_lazy('building-list')


class BuildingUpdateView(BaseUpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'forms/update_building.html'
    success_url = reverse_lazy('building-list')

    def get_context_data(self, **kwargs):
        kwargs = super(BuildingUpdateView, self).get_context_data()
        asset = self.object
        content_type = ContentType.objects.get_for_model(asset)
        asset_id = asset.asset_id

        kwargs.update({
            'repairs': models.AssetRepair.objects.filter(object_id=asset_id, content_type=content_type),
            'revaluations': models.AssetRevaluationRecord.objects.filter(object_id=asset_id, content_type=content_type)
        })
        return kwargs


class BuildingListView(BaseListView):
    model = Building
    template_name = 'building_list.html'
    context_object_name = 'buildings'
    queryset = Building.objects.filter(is_disposed=False, pending_disposal=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional variables to the context
        context['form'] = AssetRevaluationForm()
        context['total_dep'] = calculate_acc_dep(Building)
        context['total_value'] = calculate_total_cost(Building)
        context['total_repair'] = calculate_total_repair(Building)
        return context


class BuildingDisposalView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Building, pk=pk)
        form = DisposeAssetForm()
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Building, pk=pk)
        form = DisposeAssetForm(request.POST, request.FILES)
        if form.is_valid():
            disposal_date = form.cleaned_data['disposal_date']
            disposal_price = form.cleaned_data['disposal_price']
            disposal_type = form.cleaned_data['disposal_type']
            reason = form.cleaned_data['reason']
            # attachment1 = form.cleaned_data['attachment1']
            # attachment2 = form.cleaned_data['attachment2']
            asset.dispose_building(disposal_date, disposal_type, disposal_price, reason)
            return redirect('pending-disposal')
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})


class BuildingRepairView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Building, pk=pk)
        form = RepairAssetForm()
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Building, pk=pk)
        form = RepairAssetForm(request.POST, request.FILES)
        if form.is_valid():
            repair_date = form.cleaned_data['repair_date']
            repair_cost = form.cleaned_data['repair_cost']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            repair_quote = form.cleaned_data['repair_quote']
            asset.repair_building(repair_date, repair_cost, description, status, repair_quote)
            return redirect('repair-pending')
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})


class BuildingRevaluateAssetsView(View):
    def get(self, request):
        return redirect('building-list')

    def post(self, request):
        form = AssetRevaluationForm(request.POST)
        if form.is_valid():
            revaluation.revaluate_all_buildings(form.cleaned_data['percentage'], form.cleaned_data['remarks'],
                                                request.user.full_name)
            return redirect('building-list')
        else:
            return reverse_lazy('building-list')


class BuildingTransferView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Building, pk=pk)
        form = TransferAssetForm()
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Building, pk=pk)
        form = TransferAssetForm(request.POST)
        if form.is_valid():
            transfer_date = form.cleaned_data['transfer_date']
            transfer_to = form.cleaned_data['transfer_to']
            transfer_from = form.cleaned_data['transfer_from']
            remarks = form.cleaned_data['remarks']
            asset.transfer_building(transfer_date, transfer_to, transfer_from, remarks)
            return redirect('transfer-pending')
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})


# MotorVehicle
class MotorVehicleCreateView(BaseCreateView):
    model = MotorVehicle
    form_class = MotorVehicleForm
    template_name = 'forms/add_motor_vehicle.html'
    success_url = reverse_lazy('motor-vehicle-list')


class MotorVehicleUpdateView(BaseUpdateView):
    model = MotorVehicle
    form_class = MotorVehicleForm
    template_name = 'forms/update_motor_vehicles.html'
    success_url = reverse_lazy('motor-vehicle-list')

    def get_context_data(self, **kwargs):
        kwargs = super(MotorVehicleUpdateView, self).get_context_data()
        asset = self.object
        content_type = ContentType.objects.get_for_model(asset)
        asset_id = asset.asset_id

        kwargs.update({
            'repairs': models.AssetRepair.objects.filter(object_id=asset_id, content_type=content_type),
            'revaluations': models.AssetRevaluationRecord.objects.filter(object_id=asset_id, content_type=content_type)
        })
        return kwargs


class MotorVehicleListView(BaseListView):
    model = MotorVehicle
    template_name = 'motorvehicles_list.html'
    context_object_name = 'motorvehicles'
    queryset = MotorVehicle.objects.filter(is_disposed=False, pending_disposal=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional variables to the context
        context['form'] = AssetRevaluationForm()
        context['total_dep'] = calculate_acc_dep(MotorVehicle)
        context['total_value'] = calculate_total_cost(MotorVehicle)
        context['total_repair'] = calculate_total_repair(MotorVehicle)
        return context


class MotorVehicleDisposalView(View):
    def get(self, request, pk):
        asset = get_object_or_404(MotorVehicle, pk=pk)
        form = DisposeAssetForm()
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(MotorVehicle, pk=pk)
        form = DisposeAssetForm(request.POST, request.FILES)
        if form.is_valid():
            disposal_date = form.cleaned_data['disposal_date']
            disposal_price = form.cleaned_data['disposal_price']
            disposal_type = form.cleaned_data['disposal_type']
            reason = form.cleaned_data['reason']
            # attachment1 = form.cleaned_data['attachment1']
            # attachment2 = form.cleaned_data['attachment2']
            asset.dispose_motor_vehicle(disposal_date, disposal_type, disposal_price, reason)
            return redirect('pending-disposal')
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})


class MotorVehicleRepairView(View):
    def get(self, request, pk):
        asset = get_object_or_404(MotorVehicle, pk=pk)
        form = RepairAssetForm()
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(MotorVehicle, pk=pk)
        form = RepairAssetForm(request.POST, request.FILES)
        if form.is_valid():
            repair_date = form.cleaned_data['repair_date']
            repair_cost = form.cleaned_data['repair_cost']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            repair_quote = form.cleaned_data['repair_quote']
            asset.repair_motor_vehicle(repair_date, repair_cost, description, status, repair_quote)
            return redirect('repair-pending')
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})


class MotorVehicleRevaluateAssetsView(View):
    def get(self, request):
        return redirect('motor-vehicle-list')

    def post(self, request):
        form = AssetRevaluationForm(request.POST)
        if form.is_valid():
            revaluation.revaluate_all_motor_vehicles(form.cleaned_data['percentage'], form.cleaned_data['remarks'],
                                                     request.user.full_name)
            return redirect('motor-vehicle-list')
        else:
            return reverse_lazy('motor-vehicle-list')


class MotorVehicleTransferView(View):
    def get(self, request, pk):
        asset = get_object_or_404(MotorVehicle, pk=pk)
        form = TransferAssetForm()
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(MotorVehicle, pk=pk)
        form = TransferAssetForm(request.POST)
        if form.is_valid():
            transfer_date = form.cleaned_data['transfer_date']
            transfer_to = form.cleaned_data['transfer_to']
            transfer_from = form.cleaned_data['transfer_from']
            remarks = form.cleaned_data['remarks']
            asset.transfer_motor_vehicle(transfer_date, transfer_to, transfer_from, remarks)
            return redirect('transfer-pending')
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})


# Machinery
class MachineryCreateView(BaseCreateView):
    model = Machinery
    form_class = MachineryForm
    template_name = 'forms/add_machinery.html'
    success_url = reverse_lazy('machinery-list')


class MachineryUpdateView(BaseUpdateView):
    model = Machinery
    form_class = MachineryForm
    template_name = 'forms/update_machinery.html'
    success_url = reverse_lazy('machinery-list')

    def get_context_data(self, **kwargs):
        kwargs = super(MachineryUpdateView, self).get_context_data()
        asset = self.object
        content_type = ContentType.objects.get_for_model(asset)
        asset_id = asset.asset_id

        kwargs.update({
            'repairs': models.AssetRepair.objects.filter(object_id=asset_id, content_type=content_type),
            'revaluations': models.AssetRevaluationRecord.objects.filter(object_id=asset_id, content_type=content_type)
        })
        return kwargs


class MachineryListView(BaseListView):
    model = Machinery
    template_name = 'machinery_list.html'
    context_object_name = 'machineries'
    queryset = Machinery.objects.filter(is_disposed=False, pending_disposal=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional variables to the context
        context['form'] = AssetRevaluationForm()
        context['total_dep'] = calculate_acc_dep(Machinery)
        context['total_value'] = calculate_total_cost(Machinery)
        context['total_repair'] = calculate_total_repair(Machinery)
        return context


class MachineryDisposalView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Machinery, pk=pk)
        form = DisposeAssetForm()
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Machinery, pk=pk)
        form = DisposeAssetForm(request.POST, request.FILES)
        if form.is_valid():
            disposal_date = form.cleaned_data['disposal_date']
            disposal_price = form.cleaned_data['disposal_price']
            disposal_type = form.cleaned_data['disposal_type']
            reason = form.cleaned_data['reason']
            # attachment1 = form.cleaned_data['attachment1']
            # attachment2 = form.cleaned_data['attachment2']
            asset.dispose_machinery(disposal_date, disposal_type, disposal_price, reason)
            return redirect('pending-disposal')
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})


class MachineryRepairView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Machinery, pk=pk)
        form = RepairAssetForm()
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Machinery, pk=pk)
        form = RepairAssetForm(request.POST, request.FILES)
        if form.is_valid():
            repair_date = form.cleaned_data['repair_date']
            repair_cost = form.cleaned_data['repair_cost']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            repair_quote = form.cleaned_data['repair_quote']
            asset.repair_machinery(repair_date, repair_cost, description, status, repair_quote)
            return redirect('repair-pending')
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})


class MachineryRevaluateAssetsView(View):
    def get(self, request):
        return redirect('machinery-list')

    def post(self, request):
        form = AssetRevaluationForm(request.POST)
        if form.is_valid():
            revaluation.revaluate_all_machinery(form.cleaned_data['percentage'], form.cleaned_data['remarks'],
                                                request.user.full_name)
            return redirect('machinery-list')
        else:
            return reverse_lazy('machinery-list')


class MachineryTransferView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Machinery, pk=pk)
        form = TransferAssetForm()
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Machinery, pk=pk)
        form = TransferAssetForm(request.POST)
        if form.is_valid():
            transfer_date = form.cleaned_data['transfer_date']
            transfer_to = form.cleaned_data['transfer_to']
            transfer_from = form.cleaned_data['transfer_from']
            remarks = form.cleaned_data['remarks']
            asset.transfer_machinery(transfer_date, transfer_to, transfer_from, remarks)
            return redirect('transfer-pending')
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})


# Furniture
class FurnitureCreateView(BaseCreateView):
    model = Furniture
    form_class = FurnitureForm
    template_name = 'forms/add_furniture.html'
    success_url = reverse_lazy('furniture-list')


class FurnitureUpdateView(BaseUpdateView):
    model = Furniture
    form_class = FurnitureForm
    template_name = 'forms/update_furniture.html'
    success_url = reverse_lazy('furniture-list')

    def get_context_data(self, **kwargs):
        kwargs = super(FurnitureUpdateView, self).get_context_data()
        asset = self.object
        content_type = ContentType.objects.get_for_model(asset)
        asset_id = asset.asset_id

        kwargs.update({
            'repairs': models.AssetRepair.objects.filter(object_id=asset_id, content_type=content_type),
            'revaluations': models.AssetRevaluationRecord.objects.filter(object_id=asset_id, content_type=content_type)
        })
        return kwargs


class FurnitureListView(BaseListView):
    model = Furniture
    template_name = 'furniture_list.html'
    context_object_name = 'furnitures'
    queryset = Furniture.objects.filter(is_disposed=False, pending_disposal=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional variables to the context
        context['form'] = AssetRevaluationForm()
        context['total_dep'] = calculate_acc_dep(Furniture)
        context['total_value'] = calculate_total_cost(Furniture)
        context['total_repair'] = calculate_total_repair(Furniture)
        return context


class FurnitureDisposalView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Furniture, pk=pk)
        form = DisposeAssetForm()
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Furniture, pk=pk)
        form = DisposeAssetForm(request.POST, request.FILES)
        if form.is_valid():
            disposal_date = form.cleaned_data['disposal_date']
            disposal_price = form.cleaned_data['disposal_price']
            disposal_type = form.cleaned_data['disposal_type']
            reason = form.cleaned_data['reason']
            # attachment1 = form.cleaned_data['attachment1']
            # attachment2 = form.cleaned_data['attachment2']
            asset.dispose_furniture(disposal_date, disposal_type, disposal_price, reason)
            return redirect('pending-disposal')
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})


class FurnitureRepairView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Furniture, pk=pk)
        form = RepairAssetForm()
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Furniture, pk=pk)
        form = RepairAssetForm(request.POST, request.FILES)
        if form.is_valid():
            repair_date = form.cleaned_data['repair_date']
            repair_cost = form.cleaned_data['repair_cost']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            repair_quote = form.cleaned_data['repair_quote']
            asset.repair_furniture(repair_date, repair_cost, description, status, repair_quote)
            return redirect('repair-pending')
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})


class FurnitureRevaluateAssetsView(View):
    def get(self, request):
        return redirect('furniture-list')

    def post(self, request):
        form = AssetRevaluationForm(request.POST)
        if form.is_valid():
            revaluation.revaluate_all_furniture(form.cleaned_data['percentage'], form.cleaned_data['remarks'],
                                                request.user.full_name)
            return redirect('furniture-list')
        else:
            return reverse_lazy('furniture-list')


class FurnitureTransferView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Furniture, pk=pk)
        form = TransferAssetForm()
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Furniture, pk=pk)
        form = TransferAssetForm(request.POST)
        if form.is_valid():
            transfer_date = form.cleaned_data['transfer_date']
            transfer_to = form.cleaned_data['transfer_to']
            transfer_from = form.cleaned_data['transfer_from']
            remarks = form.cleaned_data['remarks']
            asset.transfer_furniture(transfer_date, transfer_to, transfer_from, remarks)
            return redirect('transfer-pending')
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})


# Equipment
class EquipmentCreateView(BaseCreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'forms/add_equipment.html'
    success_url = reverse_lazy('equipment-list')


class EquipmentUpdateView(BaseUpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'forms/update_equipment.html'
    success_url = reverse_lazy('equipment-list')

    def get_context_data(self, **kwargs):
        kwargs = super(EquipmentUpdateView, self).get_context_data()
        asset = self.object
        content_type = ContentType.objects.get_for_model(asset)
        asset_id = asset.asset_id

        kwargs.update({
            'repairs': models.AssetRepair.objects.filter(object_id=asset_id, content_type=content_type),
            'revaluations': models.AssetRevaluationRecord.objects.filter(object_id=asset_id, content_type=content_type)
        })
        return kwargs

    def form_invalid(self, form):
        return HttpResponse(form.errors)


class EquipmentListView(BaseListView):
    model = Equipment
    template_name = 'equipment_list.html'
    context_object_name = 'equipments'
    queryset = Equipment.objects.filter(is_disposed=False, pending_disposal=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional variables to the context
        context['form'] = AssetRevaluationForm()
        context['total_dep'] = calculate_acc_dep(Equipment)
        context['total_value'] = calculate_total_cost(Equipment)
        context['total_repair'] = calculate_total_repair(Equipment)
        return context


class EquipmentDisposalView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Equipment, pk=pk)
        form = DisposeAssetForm()
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Equipment, pk=pk)
        form = DisposeAssetForm(request.POST, request.FILES)

        if form.is_valid():
            disposal_date = form.cleaned_data['disposal_date']
            disposal_price = form.cleaned_data['disposal_price']
            disposal_type = form.cleaned_data['disposal_type']
            reason = form.cleaned_data['reason']
            attachment1 = form.cleaned_data['attachment1']
            attachment2 = form.cleaned_data['attachment2']
            asset.dispose_equipment(disposal_date, disposal_type, disposal_price, reason)
            return redirect('pending-disposal')
        return render(request, 'forms/add_disposal.html', {'asset': asset, 'form': form})


class EquipmentRepairView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Equipment, pk=pk)
        form = RepairAssetForm()
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Equipment, pk=pk)
        form = RepairAssetForm(request.POST, request.FILES)
        if form.is_valid():
            repair_date = form.cleaned_data['repair_date']
            repair_cost = form.cleaned_data['repair_cost']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            repair_quote = form.cleaned_data['repair_quote']
            asset.repair_equipment(repair_date, repair_cost, description, status, repair_quote)
            return redirect('repair-pending')
        return render(request, 'forms/add_repair.html', {'asset': asset, 'form': form})


class EquipmentTransferView(View):
    def get(self, request, pk):
        asset = get_object_or_404(Equipment, pk=pk)
        form = TransferAssetForm()
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})

    def post(self, request, pk):
        asset = get_object_or_404(Equipment, pk=pk)
        form = TransferAssetForm(request.POST)
        if form.is_valid():
            transfer_date = form.cleaned_data['transfer_date']
            transfer_to = form.cleaned_data['transfer_to']
            transfer_from = form.cleaned_data['transfer_from']
            remarks = form.cleaned_data['remarks']
            asset.transfer_equipment(transfer_date, transfer_to, transfer_from, remarks)
            return redirect('transfer-pending')
        return render(request, 'forms/add_transfer.html', {'asset': asset, 'form': form})


class EquipmentRevaluateAssetsView(View):
    def get(self, request):
        return redirect('equipment-list')

    def post(self, request):
        form = AssetRevaluationForm(request.POST)
        if form.is_valid():
            revaluation.revaluate_all_equipment(form.cleaned_data['percentage'], form.cleaned_data['remarks'],
                                                request.user.full_name)
            return redirect('equipment-list')
        else:
            return reverse_lazy('equipment-list')


class RepairAssetApprovalView(View):
    def get(self, request, pk):
        repair = AssetRepair.objects.get(pk=pk)
        repair.approve_repair(approvedBy=request.user.full_name)
        return redirect('repair-approved')


class RepairAssetRejectionView(View):
    def get(self, request, pk):
        repair = AssetRepair.objects.get(pk=pk)
        repair.rejected_repair(approvedBy=request.user.full_name)
        return redirect('repair-rejected')

class PendingRepairListView(BaseListView):
    model = AssetRepair
    template_name = 'repairs_pending.html'
    context_object_name = 'repairs'
    queryset = AssetRepair.objects.filter(approved=False)


class ApprovedRepairListView(BaseListView):
    model = AssetRepair
    template_name = 'repairs_approved.html'
    context_object_name = 'repairs'
    queryset = AssetRepair.objects.filter(approved=True)


class RejectedRepairListView(BaseListView):
    model = AssetRepair
    template_name = 'repairs_rejected.html'
    context_object_name = 'repairs'
    queryset = AssetRepair.objects.filter(is_rejected=True)




class AssetDisposalApprovalView(View):
    def get(self, request, pk):
        disposal = AssetDisposal.objects.get(pk=pk)
        disposal.approve_disposal(approvedBy=request.user.full_name)
        return redirect('approved-disposal')


class AssetDisposalRejectionView(View):
    def get(self, request, pk):
        disposal = AssetDisposal.objects.get(pk=pk)
        disposal.reject_disposal(approvedBy=request.user.full_name)
        return redirect('rejected-disposal')


class PendingDisposalListView(BaseListView):
    model = AssetDisposal
    template_name = 'pending_disposal.html'
    context_object_name = 'assets'
    queryset = AssetDisposal.objects.filter(approved=False)


class ApprovedDisposalListView(BaseListView):
    model = AssetDisposal
    template_name = 'approved_disposal.html'
    context_object_name = 'assets'
    queryset = AssetDisposal.objects.filter(approved=True)


class RejectedDisposalListView(BaseListView):
    model = AssetDisposal
    template_name = 'rejected_disposals.html'
    context_object_name = 'assets'
    queryset = AssetDisposal.objects.filter(is_rejected=True)


class PendingTransfersListView(BaseListView):
    model = AssetTransfer
    template_name = 'pending_transfers.html'
    context_object_name = 'transfers'
    queryset = AssetTransfer.objects.filter(is_approved=False, )


class ApprovedTransfersListView(BaseListView):
    model = AssetTransfer
    template_name = 'approved_transfers.html'
    context_object_name = 'transfers'
    queryset = AssetTransfer.objects.filter(is_approved=True)


class RejectedTransfersListView(BaseListView):
    model = AssetTransfer
    template_name = 'rejected_transfers.html'
    context_object_name = 'transfers'
    queryset = AssetTransfer.objects.filter(is_rejected=True)


class TransferApprovalView(View):
    def get(self, request, pk):
        transfer = AssetTransfer.objects.get(transfer_id=pk)
        transfer.approve_transfer(approvedBy=request.user.full_name)
        return redirect('transfer-approved')


class TransferRejectionView(View):
    def get(self, request, pk):
        transfer = AssetTransfer.objects.get(transfer_id=pk)
        transfer.reject_transfer(rejectedBy=request.user.full_name)
        return redirect('transfer-rejected')


class UserListView(BaseListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


class AssetClassesListView(BaseListView):
    model = AssetClassProperties
    template_name = 'asset_class_properties.html'
    context_object_name = 'classes'


class RevaluationHistoryListView(BaseListView):
    model = AssetRevaluationRecord
    template_name = 'revaluation_history.html'
    context_object_name = 'records'


def error_404_view(request, exception):
    return render(request, '404_page.html')


def error_500_view(request, *args, **argv):
    return render(request, '500_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('/')

#
# @method_decorator(login_required, name='dispatch')
# class DataCenterView(ListView):
#     template_name = 'datacenter.html'
#     model = models.DataCenterDetail
#     queryset = models.DataCenterDetail.objects.filter(asset__is_disposed=False)
#
#
# @method_decorator(login_required, name='dispatch')
# class OfficeEquipView(ListView):
#     template_name = 'officeequipment.html'
#     model = models.OfficeEquipmentDetail
#     queryset = models.OfficeEquipmentDetail.objects.filter(asset__is_disposed=False)
#
#
# @method_decorator(login_required, name='dispatch')
# class FixtureAndFittingsView(ListView):
#     template_name = 'fixtureandfittings.html'
#     model = models.FixtureAndFittingDetail
#     queryset = models.FixtureAndFittingDetail.objects.filter(asset__is_disposed=False)
#
#
# class MotorVehiclesView(ListView):
#     template_name = 'motorvehicles_list.html'
#     model = models.MotorVehicleDetail
#     queryset = models.MotorVehicleDetail.objects.filter(asset__is_disposed=False)
#
#
# @method_decorator(login_required, name='dispatch')
# class VendorView(ListView):
#     template_name = 'vendors.html'
#     model = models.Vendor
#
#
# @method_decorator(login_required, name='dispatch')
# class MyAssetsView(ListView):
#     template_name = 'myassets.html'
#     model = models.Asset
#
#     def get_queryset(self):
#         return models.Asset.objects.filter(is_disposed=False, assignee=self.request.user)
#
#
# @method_decorator(login_required, name='dispatch')
# class DisposedAssetsView(ListView):
#     model = models.Asset
#     queryset = models.Asset.objects.filter(is_disposed=True)
#     template_name = 'disposed_assets.html'
#
#
# @method_decorator(login_required, name='dispatch')
# class MyRepairsView(ListView):
#     model = models.Repair
#     template_name = 'repairs.html'
#
#     def get_queryset(self):
#         return models.Repair.objects.filter()
#
#
# @method_decorator(login_required, name='dispatch')
# class AllRepairsView(ListView):
#     model = models.Repair
#     template_name = 'repairs.html'
#
#
# @method_decorator(login_required, name='dispatch')
# class TransferView(ListView):
#     model = models.Transfer
#     template_name = 'transfers.html'
#
#     def get_queryset(self):
#         return models.Transfer.objects.all().order_by('-created_date')
#
#
# @method_decorator(login_required, name='dispatch')
# def users_view(request):
#     return render(request, 'user_list.html')
#
#
# def logs_view(request):
#     return render(request, 'logs.html')
#
#
# @method_decorator(login_required, name='dispatch')
# class VendorUploadView(CreateView, SuccessMessageMixin):
#     http_method_names = ['post', 'get']
#     form_class = forms.CreateVendorForm
#     template_name = 'forms/vendor_upload.html'
#     success_message = "The vendor  has been created successfully"
#     success_url = "vendors"
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.save()
#         messages.success(self.request, 'You have successfully added the vendor to the system.')
#         return HttpResponseRedirect("vendors")
#
#
# @method_decorator(login_required, name='dispatch')
# class VendorUpdateView(UpdateView, SuccessMessageMixin):
#     form_class = forms.CreateVendorForm
#     model = models.Vendor
#     template_name = 'forms/update_vendor.html'
#     success_url = "vendors"
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.save()
#         messages.success(self.request, 'You have successfully updated the vendor details')
#         return HttpResponseRedirect(reverse("vendors"))
#
#
# @login_required
# def delete_vendor(request, id):
#     vendor = models.Vendor.objects.filter(vendor_id=id)
#     vendor.delete()
#     messages.warning(request, 'You have successfully deleted the vendor from the system')
#     return redirect("vendors")
#
#
# @method_decorator(login_required, name='dispatch')
# class MotorVehicleUploadView(CreateView, SuccessMessageMixin):
#     form_class = forms.CreateMotorVehicleForm
#     success_url = 'motor-vehicles'
#     template_name = 'forms/create_motor_vehicle.html'
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['vehicle'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully added the motor vehicle to the system.')
#         return HttpResponseRedirect('motor-vehicles')
#
#     def form_invalid(self, form):
#         errors = form.errors
#         messages.warning(self.request, "Please correct the errors highlighted under the fields")
#         return super(MotorVehicleUploadView, self).form_invalid(form)
#
#
# @method_decorator(login_required, name='dispatch')
# class MotorVehicleUpdateView(UpdateView, SuccessMessageMixin):
#     template_name = 'forms/update_motor_vehicle.html'
#     model = models.MotorVehicleDetail
#     form_class = forms.CreateMotorVehicleForm
#     success_url = reverse_lazy('motor-vehicles')
#     success_message = 'The vehicle has been successfully updated'
#
#     def get_context_data(self, **kwargs):
#         kwargs = super(MotorVehicleUpdateView, self).get_context_data()
#         asset = self.object.asset
#
#         kwargs.update({
#             'repairs': models.Repair.objects.filter(asset=asset),
#             'transfers': models.Transfer.objects.filter(asset=asset)
#         })
#         return kwargs
#
#     def get_form_kwargs(self):
#         kwargs = super(MotorVehicleUpdateView, self).get_form_kwargs()
#         kwargs.update(instance={
#             'vehicle': self.object,
#             'asset': self.object.asset
#         })
#         return kwargs
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['vehicle'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully updated the motor vehicle details.')
#         return HttpResponseRedirect(reverse('motor-vehicles'))
#
#
# @method_decorator(login_required, name='dispatch')
# class OfficeEquipUploadView(CreateView, SuccessMessageMixin):
#     form_class = forms.CreateOfficeEquipmentForm
#     success_url = 'office-equipment'
#     template_name = 'forms/create_office_equip.html'
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['office'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully added the office equipment to the system.')
#         return HttpResponseRedirect('office-equipment')
#
#     def form_invalid(self, form):
#         errors = form.errors
#         messages.warning(self.request, "Please correct the errors highlighted under the fields")
#         return super(OfficeEquipUploadView, self).form_invalid(form)
#
#
# @method_decorator(login_required, name='dispatch')
# class OfficeEquipUpdateView(UpdateView, SuccessMessageMixin):
#     template_name = 'forms/update_office_equipment.html'
#     model = models.OfficeEquipmentDetail
#     form_class = forms.CreateOfficeEquipmentForm
#     success_url = reverse_lazy('office-equipment')
#
#     def get_context_data(self, **kwargs):
#         kwargs = super(OfficeEquipUpdateView, self).get_context_data()
#         asset = self.object.asset
#
#         kwargs.update({
#             'repairs': models.Repair.objects.filter(asset=asset),
#             'transfers': models.Transfer.objects.filter(asset=asset)
#         })
#         return kwargs
#
#     def get_form_kwargs(self):
#         kwargs = super(OfficeEquipUpdateView, self).get_form_kwargs()
#         kwargs.update(instance={
#             'office': self.object,
#             'asset': self.object.asset
#         })
#         return kwargs
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['office'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully updated the office equipment.')
#         return HttpResponseRedirect(reverse('office-equipment'))
#
#
# @method_decorator(login_required, name='dispatch')
# class FixtureAndFittingsUploadView(CreateView, SuccessMessageMixin):
#     form_class = forms.CreateFixtureAndFittingsForm
#     success_url = 'fixture-fittings'
#     template_name = 'forms/create_fixture_and_fitting.html'
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['fitting'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully added the fixture and fitting to the system.')
#         return HttpResponseRedirect('fixture-fittings')
#
#     def form_invalid(self, form):
#         errors = form.errors
#         messages.warning(self.request, "Please correct the errors highlighted under the fields")
#         return super(FixtureAndFittingsUploadView, self).form_invalid(form)
#
#
# @method_decorator(login_required, name='dispatch')
# class FixtureAndFittingUpdateView(UpdateView, SuccessMessageMixin):
#     template_name = 'forms/update_fixture_and_fitting.html'
#     model = models.FixtureAndFittingDetail
#     form_class = forms.CreateFixtureAndFittingsForm
#     success_url = reverse_lazy('fixture-fittings')
#
#     def get_context_data(self, **kwargs):
#         kwargs = super(FixtureAndFittingUpdateView, self).get_context_data()
#         asset = self.object.asset
#
#         kwargs.update({
#             'repairs': models.Repair.objects.filter(asset=asset),
#             'transfers': models.Transfer.objects.filter(asset=asset)
#         })
#         return kwargs
#
#     def get_form_kwargs(self):
#         kwargs = super(FixtureAndFittingUpdateView, self).get_form_kwargs()
#         kwargs.update(instance={
#             'fitting': self.object,
#             'asset': self.object.asset
#         })
#         return kwargs
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['fitting'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully updated the fixture and fitting details.')
#         return HttpResponseRedirect(reverse('fixture-fittings'))
#
#
# @method_decorator(login_required, name='dispatch')
# class ComputerUploadView(CreateView, SuccessMessageMixin):
#     form_class = forms.CreateComputerEquipForm
#     success_url = 'computer-equipment'
#     template_name = 'forms/create_computer_equip.html'
#     success_message = 'The computer equipment has been added'
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['computer'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully added the computer equipment to the system.')
#         return HttpResponseRedirect('computer-equipment')
#
#     def form_invalid(self, form):
#         errors = form.errors
#         messages.warning(self.request, "Please correct the errors highlighted under the fields")
#         return super(ComputerUploadView, self).form_invalid(form)
#
#
# @method_decorator(login_required, name='dispatch')
# class ComputerEquipmentUpdateView(UpdateView, SuccessMessageMixin):
#     template_name = 'forms/update_computer_equipment.html'
#     model = models.ComputerEquipmentDetail
#     form_class = forms.CreateComputerEquipForm
#     success_url = reverse_lazy('computer-equipment')
#     success_message = 'The computer equipment has been successfully updated'
#
#     def get_context_data(self, **kwargs):
#         kwargs = super(ComputerEquipmentUpdateView, self).get_context_data()
#         asset = self.object.asset
#
#         kwargs.update({
#             'repairs': models.Repair.objects.filter(asset=asset),
#             'transfers': models.Transfer.objects.filter(asset=asset)
#         })
#         return kwargs
#
#     def get_form_kwargs(self):
#         kwargs = super(ComputerEquipmentUpdateView, self).get_form_kwargs()
#         kwargs.update(instance={
#             'computer': self.object,
#             'asset': self.object.asset
#         })
#         return kwargs
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['computer'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully updated the computer equipment.')
#         return HttpResponseRedirect(reverse('computer-equipment'))
#
#
# @method_decorator(login_required, name='dispatch')
# class DataCenterUploadView(CreateView, SuccessMessageMixin):
#     form_class = forms.CreateDataCenterEquipForm
#     success_url = 'data-center'
#     template_name = 'forms/create_datacenter_equip.html'
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['datacenter'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully added the datacenter equipment to the system.')
#         return HttpResponseRedirect('data-center')
#
#     def form_invalid(self, form):
#         errors = form.errors
#         messages.warning(self.request, "Please correct the errors highlighted under the fields")
#         return super(DataCenterUploadView, self).form_invalid(form)
#
#
# @method_decorator(login_required, name='dispatch')
# class DataCenterUpdateView(UpdateView, SuccessMessageMixin):
#     template_name = 'forms/update_datacenter_equip.html'
#     model = models.DataCenterDetail
#     form_class = forms.CreateDataCenterEquipForm
#     success_url = reverse_lazy('data-center')
#
#     def get_context_data(self, **kwargs):
#         kwargs = super(DataCenterUpdateView, self).get_context_data()
#         asset = self.object.asset
#
#         kwargs.update({
#             'repairs': models.Repair.objects.filter(asset=asset),
#             'transfers': models.Transfer.objects.filter(asset=asset)
#         })
#         return kwargs
#
#     def get_form_kwargs(self):
#         kwargs = super(DataCenterUpdateView, self).get_form_kwargs()
#         kwargs.update(instance={
#             'datacenter': self.object,
#             'asset': self.object.asset
#         })
#         return kwargs
#
#     def form_valid(self, form):
#         asset = form['asset'].save()
#         mv_details = form['datacenter'].save(commit=False)
#         mv_details.asset = asset
#         mv_details.save()
#         messages.success(self.request, 'You have successfully updated the datacenter equipment.')
#         return HttpResponseRedirect(reverse('data-center'))
#
#
# @method_decorator(login_required, name='dispatch')
# class RepairUploadView(CreateView, SuccessMessageMixin):
#     form_class = forms.CreateRepairForm
#     model = models.Repair
#     success_url = 'repairs'
#     template_name = 'forms/create_repair.html'
#
#     def form_valid(self, form):
#         asset = get_object_or_404(models.Asset, pk=self.kwargs['asset_id'])
#         form.instance.asset = asset
#         form.save()
#         messages.success(self.request, 'You have successfully added the asset repair to the system.')
#         return HttpResponseRedirect(reverse('repairs'))
#
#
# @method_decorator(login_required, name='dispatch')
# class RepairUpdateView(UpdateView, SuccessMessageMixin):
#     form_class = forms.CreateRepairForm
#     model = models.Repair
#     success_url = 'repairs'
#     template_name = 'forms/update_repair.html'
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['instance'] = self.get_object()
#         return kwargs
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.save()
#         messages.success(self.request, 'You have successfully updated the repair details.')
#         return HttpResponseRedirect(reverse("repairs"))
#
#
# @method_decorator(login_required, name='dispatch')
# class DisposalView(CreateView, SuccessMessageMixin):
#     form_class = forms.CreateDisposalForm
#     model = models.Disposal
#     success_url = 'disposed'
#     template_name = 'forms/create_disposal.html'
#
#     def form_valid(self, form):
#         asset = get_object_or_404(models.Asset, pk=self.kwargs['asset_id'])
#         form.instance.asset = asset
#         form.save()
#         asset.is_disposed = True
#         asset.save()
#         messages.success(self.request, 'The asset has been successfully disposed')
#         return HttpResponseRedirect(reverse('disposed'))
