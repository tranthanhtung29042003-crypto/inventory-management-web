from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
# Create your models here.
class ExportOrder(models.Model):
    code = models.CharField(max_length=50, unique=True)  # mã phiếu
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    customer_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code