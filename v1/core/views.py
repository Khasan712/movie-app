from drf_yasg import openapi
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from .models import Genre, Category, Cinema, CadreCinema, Series
from .serializers import (
    GenreSerializerV1, CategorySerializerV1, CinemaReadOnlySerializerV1, CinemaWriteOnlySerializerV1,
    CinemaDetailReadOnlySerializerV1, CinemaCadreSerializerV1, CadreCreateSerializerV1,
    SeriesWriteOnlySerializerV1, SeriesDetailReadOnlySerializerV1, SeriesReadOnlySerializerV1
)
from rest_framework import viewsets, mixins
from v1.utils.permissions import IsAdmin


class SeriesApiV1(viewsets.ModelViewSet):
    queryset = Series.objects.select_related('genre', 'category').order_by('-id')

    def get_queryset(self):
        if self.lookup_field not in self.kwargs:
            return super().get_queryset().filter(parent__isnull=True)
        return super().get_queryset()

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            if self.lookup_field in self.kwargs:
                return SeriesDetailReadOnlySerializerV1
            return SeriesReadOnlySerializerV1
        return SeriesWriteOnlySerializerV1


class CadreCinemaApiV1(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CadreCinema.objects.filter(cinema__isnull=False, series__isnull=True)
    serializer_class = CadreCreateSerializerV1


class CinemaApiV1(viewsets.ModelViewSet):
    queryset = Cinema.objects.select_related('genre', 'category').order_by('-id')
    permission_classes = (IsAdmin,)

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            if self.lookup_field in self.kwargs:
                return CinemaDetailReadOnlySerializerV1
            return CinemaReadOnlySerializerV1
        return CinemaWriteOnlySerializerV1


class GenreAdminApiV1(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializerV1
    permission_classes = (IsAdmin,)

    search_param = openapi.Parameter(
        'q', in_=openapi.IN_QUERY, description='Search ...', required=False, type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[search_param])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.query_params.get('q')
        filter_data = Q()

        if q:
            filter_data &= Q(name__icontains=q)

        return super().get_queryset().filter(filter_data)


class CategoryAdminApiV1(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializerV1
    permission_classes = (IsAdmin,)

    search_param = openapi.Parameter(
        'q', in_=openapi.IN_QUERY, description='Search ...', required=False, type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[search_param])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.query_params.get('q')
        filter_data = Q()

        if q:
            filter_data &= Q(name__icontains=q)

        return super().get_queryset().filter(filter_data)
