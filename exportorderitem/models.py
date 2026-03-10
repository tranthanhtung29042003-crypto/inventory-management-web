from django.db import models
from exportorder.models import ExportOrder
from product.models import Product


class ExportOrderItem(models.Model):
    export_order = models.ForeignKey(ExportOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name