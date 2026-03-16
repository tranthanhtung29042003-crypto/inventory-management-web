from django.conf import settings
from django.db import models
from supplier.models import Supplier

from .services.generate_importoder_code import generate_importoder_code


class ImportOrder(models.Model):
    code = models.CharField(max_length=50, unique=True, default=generate_importoder_code)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    note = models.CharField(max_length=200, blank=True, null=True)

    invoice_file = models.FileField(
        upload_to='import/invoices/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code