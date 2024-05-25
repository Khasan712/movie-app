from django.urls import path
from .views import CustomerRegisterApiV1, CustomLoginApiV1, MeApiV1


urlpatterns = [
    path('me/', MeApiV1.as_view()),
    path('login/', CustomLoginApiV1.as_view()),
    path('customer-register/', CustomerRegisterApiV1.as_view()),
]
