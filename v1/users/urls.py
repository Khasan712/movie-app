from django.urls import path
from .views import CustomerRegisterApiV1, CustomLoginApiV1


urlpatterns = [
    path('login/', CustomLoginApiV1.as_view()),
    path('customer-register/', CustomerRegisterApiV1.as_view()),
]
