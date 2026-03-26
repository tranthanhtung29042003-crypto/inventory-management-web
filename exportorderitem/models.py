from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from exportorder.models import ExportOrder


from productwarehouse.models import ProductWarehouse

from product.models import Product


class ExportOrderItem(models.Model):

    export_order = models.ForeignKey(
        ExportOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    warehouse = models.ForeignKey(ProductWarehouse, on_delete=models.CASCADE)

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
        if self.warehouse and self.quantity:

            stock = self.warehouse.quantity  # ✅ lấy trực tiếp

            if self.quantity > stock:
                raise ValidationError(
                    f"{self.warehouse.product.name} chỉ còn {stock} trong kho"
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # 🔥 đảm bảo validation chạy
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['export_order']),
        ]