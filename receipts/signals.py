# items/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from receipts.models import Item  # your existing Item model
from receipts.models import Product, ItemNameProduct


@receiver(post_save, sender=Item)
def ensure_product_for_item(sender, instance: Item, created, **kwargs):
    """
    When an Item row is created (or updated), ensure there's a Product
    for its name and a ItemNameProduct mapping.
    """
    name = instance.name or ""
    if not name:
        return

    # get_or_create product
    product, _ = Product.objects.get_or_create(name=name)

    # create mapping if missing
    ItemNameProduct.objects.get_or_create(
        item_name=name, defaults={"product": product})
