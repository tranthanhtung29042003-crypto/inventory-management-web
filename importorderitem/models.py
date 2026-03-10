from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField, DecimalField

from importorder.models import ImportOrder
from product.models import Product



# Create your models here.
class ImportOrderItem(models.Model):
    import_order = models.ForeignKey(ImportOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)