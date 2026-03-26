from django.db import models
from importorder.models import ImportOrder
from product.models import Product

from warehouse.models import Warehouse


class ImportOrderItem(models.Model):
    import_order = models.ForeignKey(
        ImportOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.quantity and self.unit_price:
            self.subtotal = self.quantity * self.unit_price
        else:
            self.subtotal = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

