from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class SerializerRaise400(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Error occurred.')
    default_code = 'invalid'
