# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from users.models import User
# from core.models import MotorVehicleDetail, OfficeEquipmentDetail, FixtureAndFittingDetail, DataCenterDetail, \
#     ComputerEquipmentDetail, Asset, Vendor, Transfer
# from django.core.mail import EmailMessage
# import threading
#
#
# class EmailThread(threading.Thread):
#     def __init__(self, email):
#         super().__init__()
#         self.email = email
#         threading.Thread.__init__(self)
#
#     def run(self):
#         self.email.send(fail_silently=False)
#
#
# def custom_send_email(asset):
#     print(vars(asset))
#     subject = "Asset Assignment"
#     to_email = ["{}".format(asset.assignee.email)]
#     cc = ['giftm@kenac.co.zw', 'mercyc@kenac.co.zw']
#     message = ''
#     try:
#         g = asset.vehicle_details
#         message = "Good day {0}\n " \
#                   " You have been assigned the following motor vehicle with \n" \
#                   "\n" \
#                   "\n" \
#                   "\n" \
#                   "Asset Name: {1} \n" \
#                   "Registration Number : {2}\n" \
#                   "Engine Number: {3}\n" \
#                   "Chassis Number: {4} \n" \
#                   "\n" \
#                   "\n" \
#                   "\n" \
#                   "Please Log Into the system and view your assigned assets" \
#                   "\n" \
#                   "http://10.10.0.57:8005/my-assets".format(asset.assignee.full_name,
#                                                             asset.name,
#                                                             asset.vehicle_details.reg_number,
#                                                             asset.vehicle_details.engine_number,
#                                                             asset.vehicle_details.chassis_number
#                                                             )
#         print(message)
#     except:
#         pass
#
#     try:
#         g = asset.office_details
#         message = "Good day {0}\n" \
#                   "\n " \
#                   "\n" \
#                   "\n" \
#                   "You have been assigned an office equipment with \n" \
#                   "\n" \
#                   "Asset Name: {1}\n" \
#                   "Asset Id : {2}\n" \
#                   "Asset Tag: {3}\n" \
#                   "\n" \
#                   "\n" \
#                   "\n" \
#                   "Please Log Into the system and view your assigned assets \n" \
#                   "\n" \
#                   "http://10.10.0.57:8005/my-assets".format(asset.assignee.full_name,
#                                                             asset.name,
#                                                             asset.asset_id,
#                                                             asset.office_details.asset_tag)
#         print(message)
#     except:
#         pass
#
#     try:
#         g = asset.fixture_details
#         message = "Good day {0}\n" \
#                   "\n " \
#                   "\n" \
#                   "\n" \
#                   "You have been assigned a fixture and fitting with \n" \
#                   "Asset Name: {1}\n" \
#                   "Asset Id : {2}\n" \
#                   "Asset Tag: {3}\n" \
#                   "\n" \
#                   "\n" \
#                   "\n" \
#                   "Please Log Into the system and view your assigned assets \n" \
#                   "\n" \
#                   "http://10.10.0.57:8005/my-assets".format(asset.assignee.full_name,
#                                                             asset.name,
#                                                             asset.asset_id,
#                                                             asset.fixture_detail.asset_tag)
#         print(message)
#     except:
#         pass
#
#     try:
#         g = asset.datacenter_details
#         message = "Good day {0}\n" \
#                   "\n " \
#                   "\n" \
#                   "\n" \
#                   "You have been assigned a datacenter equipment with \n" \
#                   "Asset Name: {1}\n" \
#                   "Asset Id : {2}\n" \
#                   "Serial Number: {3}\n" \
#                   "\n" \
#                   "\n" \
#                   "\n" \
#                   "Please Log Into the system and view your assigned assets \n" \
#                   "\n" \
#                   "http://10.10.0.57:8005/my-assets".format(asset.assignee.full_name,
#                                                             asset.name,
#                                                             asset.asset_id,
#                                                             asset.datacenter_details.serial_number)
#         print(message)
#     except:
#         pass
#
#     try:
#         g = asset.computer_details
#         message = "Good day {0}\n" \
#                   "\n " \
#                   "\n" \
#                   "\n" \
#                   "You have been assigned a computer equipment with \n" \
#                   "Asset Name: {1}\n" \
#                   "Asset Id : {2}\n" \
#                   "Serial Number: {3}\n" \
#                   "\n" \
#                   "\n" \
#                   "\n" \
#                   "Please Log Into the system and view your assigned assets \n" \
#                   "\n" \
#                   "http://10.10.0.57:8005/my-assets".format(asset.assignee.full_name,
#                                                             asset.name,
#                                                             asset.asset_id,
#                                                             asset.computer_details.serial_number)
#         print(message)
#     except:
#         pass
#
#     email = EmailMessage(
#         subject=subject,
#         to=to_email,
#         cc=cc,
#         body=message,
#         from_email='kenac-asset-manager@outlook.com'
#     )
#     # EmailThread(email=email).start()
#
#
# @receiver(pre_save, sender=Asset)
# def pre_save_asset(sender, instance, **kwargs):
#     # Checks if updated asset has an assignee
#     if instance.assignee is not None:
#         old_obj = Asset.objects.filter(asset_id=instance.asset_id)
#         # This statement checks if asset is a new asset
#         if old_obj.exists():
#             old_asset = Asset.objects.get(asset_id=instance.asset_id)
#             # Checks if old asset has an assignee
#             if old_asset.assignee is not None:
#                 # Checks if old asset email is same is new email
#                 if old_asset.assignee.email == instance.assignee.email:
#                     pass
#                 # If emails are different create transfer instance
#                 else:
#                     transfer = Transfer.objects.create(
#                         asset=instance,
#                         transfer_to="{0} {1}".format(instance.assignee.first_name, instance.assignee.last_name),
#                         transfer_from=old_asset.assignee.full_name
#                     )
#             # Old asset was not assigned hence create Transfer instance with None
#             else:
#                 transfer = Transfer.objects.create(
#                     asset=instance,
#                     transfer_to="{0} {1}".format(instance.assignee.first_name, instance.assignee.last_name),
#                     transfer_from="Unassigned"
#                 )
#                 transfer.save()
#         else:
#             pass
#
#     else:
#         old_obj = Asset.objects.filter(asset_id=instance.asset_id)
#         if old_obj.exists():
#             old_asset = Asset.objects.get(asset_id=instance.asset_id)
#
#             if old_asset.assignee is not None:
#                 transfer = Transfer.objects.create(
#                     asset=instance,
#                     transfer_to="Unassigned",
#                     transfer_from=old_asset.assignee.full_name
#                 )
#                 transfer.save()
#
#             else:
#                 pass
#
#
# @receiver(post_save, sender=Asset)
# def post_save_asset(sender, instance, created, **kwargs):
#     if created:
#         if instance.assignee is not None:
#             transfer = Transfer.objects.create(
#                 asset=instance,
#                 transfer_to=instance.assignee.full_name,
#                 transfer_from="Unassigned"
#             )
#             transfer.save()
#             print("I am here")
#
#
#         else:
#
#             old_obj = Asset.objects.filter(asset_id=instance.asset_id)
#             if old_obj.exists():
#                 old_asset = Asset.objects.get(asset_id=instance.asset_id)
#
#                 if old_asset.assignee is not None:
#                     custom_send_email(instance)
#                     transfer = Transfer.objects.create(
#                         asset=instance,
#                         transfer_to="Unassigned",
#                         transfer_from=old_asset.assignee.full_name
#                     )
#                     transfer.save()
#
#
#                 else:
#                     pass
#     else:
#         pass
#
#
# @receiver(post_save, sender=Transfer)
# def transfer_post_save(sender, instance, created, **kwargs):
#     if created:
#         if instance.transfer_to != "Unassigned":
#             custom_send_email(instance.asset)
