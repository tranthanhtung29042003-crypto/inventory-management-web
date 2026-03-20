from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        STAFF = "STAFF", "Staff"

    phone = models.CharField(max_length=20, null=True, blank=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.username} ({self.email})"