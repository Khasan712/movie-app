from django.db import models
from django.utils.translation import gettext_lazy as _

from v1.commons.enums import SourceType


class CustomBaseAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

