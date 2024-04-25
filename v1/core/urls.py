from .views import (
    GenreAdminApiV1, CategoryAdminApiV1, CinemaApiV1, CadreCinemaApiV1, SeriesApiV1, BannerApiV1, MyListApiV1,
    TopCinemaApiV1
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('admin/genre', GenreAdminApiV1)
router.register('admin/category', CategoryAdminApiV1)
router.register('admin/cinema', CinemaApiV1)
router.register('admin/cadre', CadreCinemaApiV1)
router.register('admin/series', SeriesApiV1)
router.register('banner', BannerApiV1)
router.register('my-list', MyListApiV1)
router.register('top-cinema', TopCinemaApiV1)

urlpatterns = router.urls
