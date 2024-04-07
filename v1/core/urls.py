from django.urls import path
from .views import GenreAdminApiV1, CategoryAdminApiV1
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('admin/genre', GenreAdminApiV1)
router.register('admin/category', CategoryAdminApiV1)

urlpatterns = router.urls
