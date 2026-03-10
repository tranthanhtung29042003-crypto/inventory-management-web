
from django.contrib.auth.models import User
from django.db import models
from django.forms import DecimalField
from django.conf import settings
from supplier.models import Supplier


# Create your models here.
class ImportOrder(models.Model):
    code = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    total_amount = DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=200)
    invoice_file = models.FileField(upload_to='import/invoices/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)