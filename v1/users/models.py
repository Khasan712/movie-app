from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from v1.commons.enums import UserRole
from v1.users.managers import (AdminManager, CustomerManager, CustomManager)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices(), default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"

    objects = CustomManager()

    def __str__(self) -> str:
        return self.phone_number


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True


class Customer(User):
    objects = CustomerManager()

    class Meta:
        proxy = True

