from django.db import models

from product.models import Product
from warehouse.models import Warehouse


# Create your models here.
class ProductWarehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)