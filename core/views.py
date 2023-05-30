import json

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import CreateView, ListView, UpdateView
from core import models, forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q, Sum
from django.contrib import messages


def sum_value(object_list):
    sum = 0
    for asset in object_list:
        sum += asset.current_value

    return sum


def error_404_view(request, exception):
    return render(request, '404_page.html')


def error_500_view(request, *args, **argv):
    return render(request, '500_page.html')


# Function to filter warranty dates
def warranty_days(equip):
    days_left = equip.warranty_days
    return days_left


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def index(request):
    transfers = models.Transfer.objects.all().order_by('-created_date')[:4]
    vehicles = models.MotorVehicleDetail.objects.filter(asset__is_disposed=False)
    fittings = models.FixtureAndFittingDetail.objects.filter(asset__is_disposed=False)
    office_equip = models.OfficeEquipmentDetail.objects.filter(asset__is_disposed=False)
    datacenter_equip = models.DataCenterDetail.objects.filter(asset__is_disposed=False)
    comp_equip = models.ComputerEquipmentDetail.objects.filter(asset__is_disposed=False)

    vehicles_num = vehicles.count()
    fittings_num = fittings.count()
    office_equip_num = office_equip.count()
    datacenter_equip_num = datacenter_equip.count()
    comp_equip_num = comp_equip.count()

    vehicles_value = sum_value(vehicles)
    fittings_value = sum_value(fittings)
    office_value = sum_value(office_equip)
    datacenter_value = sum_value(datacenter_equip)
    computer_value = sum_value(comp_equip)
    total_valuation = vehicles_value + fittings_value + office_value + datacenter_value + computer_value

    computers = models.ComputerEquipmentDetail.objects.filter(asset__is_disposed=False)
    datacenter = models.DataCenterDetail.objects.filter(asset__is_disposed=False)
    comp_active = []
    comp_inactive = []
    comp_critical = []
    dc_active = []
    dc_inactive = []
    dc_critical = []

    for equip in computers:
        days_left = warranty_days(equip)

        if days_left > 30:
            comp_active.append(equip)

        elif days_left >= 0:
            comp_critical.append(equip)

        else:
            comp_inactive.append(equip)

    for equip in datacenter:
        days_left = warranty_days(equip)

        if days_left > 30:
            dc_active.append(equip)

        elif days_left >= 0:
            dc_critical.append(equip)

        else:
            dc_inactive.append(equip)
    tot_inactive = len(dc_inactive) + len(comp_inactive)
    tot_active = len(comp_active) + len(dc_active)
    tot_critical = len(comp_critical) + len(dc_critical)
    repairs_total = models.Repair.objects.all().count()
    completed_repairs = models.Repair.objects.filter(status='COMPLETED').count()
    repair_percentage = 0
    try:
        repair_percentage = int(completed_repairs / repairs_total * 100)
    except ZeroDivisionError:
        pass

    total_asset_num = models.Asset.objects.filter(is_disposed=False).count()

    disposed_assets = models.Asset.objects.filter(is_disposed=True).count()
    unassigned_assets = models.Asset.objects.filter(is_disposed=False, assignee=None).count()

    vendors = models.Vendor.objects.all().count()

    context = {
        'transfers': transfers,
        'assets_sum': total_asset_num,
        'vehicles_num': vehicles_num,
        'fittings_num': fittings_num,
        'office_num': office_equip_num,
        'datacenter_num': datacenter_equip_num,
        'computer_num': comp_equip_num,
        'total_asset_num': total_asset_num,
        'disposed_assets': disposed_assets,
        'unassigned_assets': unassigned_assets,
        'warranty_critical': tot_critical,
        'warranty_active': tot_active,
        'warranty_expired': tot_inactive,
        'total_value': total_valuation,
        'computer_value': computer_value,
        'datacenter_value': datacenter_value,
        'office_value': office_value,
        'vehicles_value': vehicles_value,
        'fittings_value': fittings_value
    }
    return render(request, 'index.html', context=context)


@method_decorator(login_required, name='dispatch')
class ComputerEquipView(ListView):
    template_name = 'computerequipment.html'
    model = models.ComputerEquipmentDetail
    queryset = models.ComputerEquipmentDetail.objects.filter(asset__is_disposed=False)


@method_decorator(login_required, name='dispatch')
class DataCenterView(ListView):
    template_name = 'datacenter.html'
    model = models.DataCenterDetail
    queryset = models.DataCenterDetail.objects.filter(asset__is_disposed=False)


@method_decorator(login_required, name='dispatch')
class OfficeEquipView(ListView):
    template_name = 'officeequipment.html'
    model = models.OfficeEquipmentDetail
    queryset = models.OfficeEquipmentDetail.objects.filter(asset__is_disposed=False)


@method_decorator(login_required, name='dispatch')
class FixtureAndFittingsView(ListView):
    template_name = 'fixtureandfittings.html'
    model = models.FixtureAndFittingDetail
    queryset = models.FixtureAndFittingDetail.objects.filter(asset__is_disposed=False)


class MotorVehiclesView(ListView):
    template_name = 'motorvehicles.html'
    model = models.MotorVehicleDetail
    queryset = models.MotorVehicleDetail.objects.filter(asset__is_disposed=False)


@method_decorator(login_required, name='dispatch')
class VendorView(ListView):
    template_name = 'vendors.html'
    model = models.Vendor


@method_decorator(login_required, name='dispatch')
class MyAssetsView(ListView):
    template_name = 'myassets.html'
    model = models.Asset

    def get_queryset(self):
        return models.Asset.objects.filter(is_disposed=False, assignee=self.request.user)


@method_decorator(login_required, name='dispatch')
class DisposedAssetsView(ListView):
    model = models.Asset
    queryset = models.Asset.objects.filter(is_disposed=True)
    template_name = 'disposed_assets.html'


@method_decorator(login_required, name='dispatch')
class MyRepairsView(ListView):
    model = models.Repair
    template_name = 'repairs.html'

    def get_queryset(self):
        return models.Repair.objects.filter()


@method_decorator(login_required, name='dispatch')
class AllRepairsView(ListView):
    model = models.Repair
    template_name = 'repairs.html'


@method_decorator(login_required, name='dispatch')
class TransferView(ListView):
    model = models.Transfer
    template_name = 'transfers.html'

    def get_queryset(self):
        return models.Transfer.objects.all().order_by('-created_date')


@method_decorator(login_required, name='dispatch')
def users_view(request):
    return render(request, 'user_list.html')


def logs_view(request):
    return render(request, 'logs.html')


@method_decorator(login_required, name='dispatch')
class VendorUploadView(CreateView, SuccessMessageMixin):
    http_method_names = ['post', 'get']
    form_class = forms.CreateVendorForm
    template_name = 'forms/vendor_upload.html'
    success_message = "The vendor  has been created successfully"
    success_url = "vendors"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        messages.success(self.request, 'You have successfully added the vendor to the system.')
        return HttpResponseRedirect("vendors")


@method_decorator(login_required, name='dispatch')
class VendorUpdateView(UpdateView, SuccessMessageMixin):
    form_class = forms.CreateVendorForm
    model = models.Vendor
    template_name = 'forms/update_vendor.html'
    success_url = "vendors"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        messages.success(self.request, 'You have successfully updated the vendor details')
        return HttpResponseRedirect(reverse("vendors"))


@login_required
def delete_vendor(request, id):
    vendor = models.Vendor.objects.filter(vendor_id=id)
    vendor.delete()
    messages.warning(request, 'You have successfully deleted the vendor from the system')
    return redirect("vendors")


@method_decorator(login_required, name='dispatch')
class MotorVehicleUploadView(CreateView, SuccessMessageMixin):
    form_class = forms.CreateMotorVehicleForm
    success_url = 'motor-vehicles'
    template_name = 'forms/create_motor_vehicle.html'

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['vehicle'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully added the motor vehicle to the system.')
        return HttpResponseRedirect('motor-vehicles')

    def form_invalid(self, form):
        errors = form.errors
        messages.warning(self.request, "Please correct the errors highlighted under the fields")
        return super(MotorVehicleUploadView, self).form_invalid(form)


@method_decorator(login_required, name='dispatch')
class MotorVehicleUpdateView(UpdateView, SuccessMessageMixin):
    template_name = 'forms/update_motor_vehicle.html'
    model = models.MotorVehicleDetail
    form_class = forms.CreateMotorVehicleForm
    success_url = reverse_lazy('motor-vehicles')
    success_message = 'The vehicle has been successfully updated'

    def get_context_data(self, **kwargs):
        kwargs = super(MotorVehicleUpdateView, self).get_context_data()
        asset = self.object.asset

        kwargs.update({
            'repairs': models.Repair.objects.filter(asset=asset),
            'transfers': models.Transfer.objects.filter(asset=asset)
        })
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(MotorVehicleUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'vehicle': self.object,
            'asset': self.object.asset
        })
        return kwargs

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['vehicle'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully updated the motor vehicle details.')
        return HttpResponseRedirect(reverse('motor-vehicles'))


@method_decorator(login_required, name='dispatch')
class OfficeEquipUploadView(CreateView, SuccessMessageMixin):
    form_class = forms.CreateOfficeEquipmentForm
    success_url = 'office-equipment'
    template_name = 'forms/create_office_equip.html'

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['office'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully added the office equipment to the system.')
        return HttpResponseRedirect('office-equipment')

    def form_invalid(self, form):
        errors = form.errors
        messages.warning(self.request, "Please correct the errors highlighted under the fields")
        return super(OfficeEquipUploadView, self).form_invalid(form)


@method_decorator(login_required, name='dispatch')
class OfficeEquipUpdateView(UpdateView, SuccessMessageMixin):
    template_name = 'forms/update_office_equipment.html'
    model = models.OfficeEquipmentDetail
    form_class = forms.CreateOfficeEquipmentForm
    success_url = reverse_lazy('office-equipment')

    def get_context_data(self, **kwargs):
        kwargs = super(OfficeEquipUpdateView, self).get_context_data()
        asset = self.object.asset

        kwargs.update({
            'repairs': models.Repair.objects.filter(asset=asset),
            'transfers': models.Transfer.objects.filter(asset=asset)
        })
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(OfficeEquipUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'office': self.object,
            'asset': self.object.asset
        })
        return kwargs

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['office'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully updated the office equipment.')
        return HttpResponseRedirect(reverse('office-equipment'))


@method_decorator(login_required, name='dispatch')
class FixtureAndFittingsUploadView(CreateView, SuccessMessageMixin):
    form_class = forms.CreateFixtureAndFittingsForm
    success_url = 'fixture-fittings'
    template_name = 'forms/create_fixture_and_fitting.html'

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['fitting'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully added the fixture and fitting to the system.')
        return HttpResponseRedirect('fixture-fittings')

    def form_invalid(self, form):
        errors = form.errors
        messages.warning(self.request, "Please correct the errors highlighted under the fields")
        return super(FixtureAndFittingsUploadView, self).form_invalid(form)


@method_decorator(login_required, name='dispatch')
class FixtureAndFittingUpdateView(UpdateView, SuccessMessageMixin):
    template_name = 'forms/update_fixture_and_fitting.html'
    model = models.FixtureAndFittingDetail
    form_class = forms.CreateFixtureAndFittingsForm
    success_url = reverse_lazy('fixture-fittings')

    def get_context_data(self, **kwargs):
        kwargs = super(FixtureAndFittingUpdateView, self).get_context_data()
        asset = self.object.asset

        kwargs.update({
            'repairs': models.Repair.objects.filter(asset=asset),
            'transfers': models.Transfer.objects.filter(asset=asset)
        })
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(FixtureAndFittingUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'fitting': self.object,
            'asset': self.object.asset
        })
        return kwargs

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['fitting'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully updated the fixture and fitting details.')
        return HttpResponseRedirect(reverse('fixture-fittings'))


@method_decorator(login_required, name='dispatch')
class ComputerUploadView(CreateView, SuccessMessageMixin):
    form_class = forms.CreateComputerEquipForm
    success_url = 'computer-equipment'
    template_name = 'forms/create_computer_equip.html'
    success_message = 'The computer equipment has been added'

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['computer'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully added the computer equipment to the system.')
        return HttpResponseRedirect('computer-equipment')

    def form_invalid(self, form):
        errors = form.errors
        messages.warning(self.request, "Please correct the errors highlighted under the fields")
        return super(ComputerUploadView, self).form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ComputerEquipmentUpdateView(UpdateView, SuccessMessageMixin):
    template_name = 'forms/update_computer_equipment.html'
    model = models.ComputerEquipmentDetail
    form_class = forms.CreateComputerEquipForm
    success_url = reverse_lazy('computer-equipment')
    success_message = 'The computer equipment has been successfully updated'

    def get_context_data(self, **kwargs):
        kwargs = super(ComputerEquipmentUpdateView, self).get_context_data()
        asset = self.object.asset

        kwargs.update({
            'repairs': models.Repair.objects.filter(asset=asset),
            'transfers': models.Transfer.objects.filter(asset=asset)
        })
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(ComputerEquipmentUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'computer': self.object,
            'asset': self.object.asset
        })
        return kwargs

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['computer'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully updated the computer equipment.')
        return HttpResponseRedirect(reverse('computer-equipment'))


@method_decorator(login_required, name='dispatch')
class DataCenterUploadView(CreateView, SuccessMessageMixin):
    form_class = forms.CreateDataCenterEquipForm
    success_url = 'data-center'
    template_name = 'forms/create_datacenter_equip.html'

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['datacenter'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully added the datacenter equipment to the system.')
        return HttpResponseRedirect('data-center')

    def form_invalid(self, form):
        errors = form.errors
        messages.warning(self.request, "Please correct the errors highlighted under the fields")
        return super(DataCenterUploadView, self).form_invalid(form)


@method_decorator(login_required, name='dispatch')
class DataCenterUpdateView(UpdateView, SuccessMessageMixin):
    template_name = 'forms/update_datacenter_equip.html'
    model = models.DataCenterDetail
    form_class = forms.CreateDataCenterEquipForm
    success_url = reverse_lazy('data-center')

    def get_context_data(self, **kwargs):
        kwargs = super(DataCenterUpdateView, self).get_context_data()
        asset = self.object.asset

        kwargs.update({
            'repairs': models.Repair.objects.filter(asset=asset),
            'transfers': models.Transfer.objects.filter(asset=asset)
        })
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(DataCenterUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'datacenter': self.object,
            'asset': self.object.asset
        })
        return kwargs

    def form_valid(self, form):
        asset = form['asset'].save()
        mv_details = form['datacenter'].save(commit=False)
        mv_details.asset = asset
        mv_details.save()
        messages.success(self.request, 'You have successfully updated the datacenter equipment.')
        return HttpResponseRedirect(reverse('data-center'))


@method_decorator(login_required, name='dispatch')
class RepairUploadView(CreateView, SuccessMessageMixin):
    form_class = forms.CreateRepairForm
    model = models.Repair
    success_url = 'repairs'
    template_name = 'forms/create_repair.html'

    def form_valid(self, form):
        asset = get_object_or_404(models.Asset, pk=self.kwargs['asset_id'])
        form.instance.asset = asset
        form.save()
        messages.success(self.request, 'You have successfully added the asset repair to the system.')
        return HttpResponseRedirect(reverse('repairs'))


@method_decorator(login_required, name='dispatch')
class RepairUpdateView(UpdateView, SuccessMessageMixin):
    form_class = forms.CreateRepairForm
    model = models.Repair
    success_url = 'repairs'
    template_name = 'forms/update_repair.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        messages.success(self.request, 'You have successfully updated the repair details.')
        return HttpResponseRedirect(reverse("repairs"))


@method_decorator(login_required, name='dispatch')
class DisposalView(CreateView, SuccessMessageMixin):
    form_class = forms.CreateDisposalForm
    model = models.Disposal
    success_url = 'disposed'
    template_name = 'forms/create_disposal.html'

    def form_valid(self, form):
        asset = get_object_or_404(models.Asset, pk=self.kwargs['asset_id'])
        form.instance.asset = asset
        form.save()
        asset.is_disposed = True
        asset.save()
        messages.success(self.request, 'The asset has been successfully disposed')
        return HttpResponseRedirect(reverse('disposed'))
