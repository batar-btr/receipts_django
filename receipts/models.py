from django.db import models


class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    receipt_number = models.TextField(unique=True, blank=True, null=True)
    date_time = models.TextField(blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'receipts'

    def __str__(self):
        return f"Receipt #{self.receipt_number or self.id} — {self.date_time}"


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    barcode = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    sum = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='items',
        db_column='receipt_id',  # matches your table column
    )

    class Meta:
        db_table = 'items'

    def __str__(self):
        return f"{self.name or 'Unnamed item'} (x{self.quantity or 0})"
