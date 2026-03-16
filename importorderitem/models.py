from django.db import models
from importorder.models import ImportOrder
from product.models import Product


class ImportOrderItem(models.Model):

    import_order = models.ForeignKey(
        ImportOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=0)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

        total = sum(
            item.subtotal
            for item in self.import_order.items.all()
        )

        self.import_order.total_amount = total
        self.import_order.save()

        product = self.product
        product.quantity_in_stock += self.quantity
        product.save()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

