from django.core.management.base import BaseCommand
from datetime import date
from core.models import BaseAsset, DepreciationEntry

class GenerateDepreciationCommand(BaseCommand):
    help = 'Generates depreciation entries for all assets'

    def handle(self, *args, **options):
        assets = BaseAsset.objects.all()

        for asset in assets:
            depreciation_amount = asset.calculate_depreciation()
            depreciation_entry = DepreciationEntry(
                asset=asset,
                depreciation_date=date.today(),
                depreciation_amount=depreciation_amount
            )
            depreciation_entry.save()

        self.stdout.write(self.style.SUCCESS('Depreciation entries generated successfully.'))
