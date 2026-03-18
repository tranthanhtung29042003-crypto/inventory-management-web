from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from exportorder.models import ExportOrder
from product.models import Product


class ExportOrderItem(models.Model):
    export_order = models.ForeignKey(
        ExportOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.export_order.code} - {self.product.name} ({self.quantity})"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def clean(self):
        if self.product and self.quantity:
            if self.product.quantity_in_stock < self.quantity:
                raise ValidationError(
                    f"{self.product.name} không đủ tồn kho"
                )

    class Meta:
        indexes = [
            models.Index(fields=['export_order']),
        ]