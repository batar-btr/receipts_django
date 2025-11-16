# items/management/commands/build_products_from_items.py
from django.core.management.base import BaseCommand
from django.db import transaction
from receipts.models import Item  # adjust import path if apps differ
from receipts.models import Product, ItemNameProduct


class Command(BaseCommand):
    help = "Create Product rows and ItemNameProduct mappings from existing Item.name values."

    def handle(self, *args, **options):
        self.stdout.write("Collecting unique item names...")
        names_qs = Item.objects.values_list("name", flat=True).distinct()
        # names = [n.strip() for n in names_qs if n and n.strip()]

        created_products = 0
        created_mappings = 0

        with transaction.atomic():
            for name in names_qs:
                product, created = Product.objects.get_or_create(name=name)
                if created:
                    created_products += 1

                mapping, mapping_created = ItemNameProduct.objects.get_or_create(
                    item_name=name,
                    defaults={"product": product}
                )

                if mapping_created:
                    created_mappings += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Products created: {created_products}, mappings created: {created_mappings}"
        ))
