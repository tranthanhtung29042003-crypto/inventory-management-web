from django.db import models

from product.models import Product
from user.models import User


# Create your models here.
class StockMovement(models.Model):

    MOVEMENT_TYPE_CHOICES = (
        ("IMPORT", "Import"),
        ("EXPORT", "Export"),
        ("ADJUST", "Adjust"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    movement_type = models.CharField(
        max_length=10,
        choices=MOVEMENT_TYPE_CHOICES
    )

    quantity = models.IntegerField()

    reference_id = models.IntegerField(null=True, blank=True)

    note = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} - {self.quantity}"