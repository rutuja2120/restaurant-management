from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_admin_user(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_staff_member(self):
        return self.role in [self.Role.ADMIN, self.Role.STAFF] or self.is_staff

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
