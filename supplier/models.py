from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.TextField()
    tax_code = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)