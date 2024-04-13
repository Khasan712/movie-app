from drf_yasg import openapi
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from .models import Genre, Category, Cinema, CadreCinema, Series, Banner, MyList
from .serializers import (
    GenreSerializerV1, CategorySerializerV1, CinemaReadOnlySerializerV1, CinemaWriteOnlySerializerV1,
    CinemaDetailReadOnlySerializerV1, CadreCreateSerializerV1,
    SeriesWriteOnlySerializerV1, SeriesDetailReadOnlySerializerV1, SeriesReadOnlySerializerV1,
    BannerCreateUpdateSerializerV1, BannerGetSerializerV1, CategoryListSerializerV1, CategorySeriesListSerializerV1,
    MyListCreateUpdateSerializerV1
)
from rest_framework import viewsets, mixins
from v1.utils.permissions import IsAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from v1.utils import const_veriables


class MyListApiV1(viewsets.ModelViewSet):
    queryset = MyList.objects.select_related('cinema', 'series', 'user').order_by('-id')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        params = self.request.query_params
        search_param = params.get('q')
        category_id = params.get('category_id')
        content_type = params.get('content_type')
        filter_data = Q(user_id=self.request.user.id)
        if search_param:
            filter_data &= (
                    Q(cinema__name__icontains=search_param) | Q(cinema__description__icontains=search_param) |
                    Q(series__name__icontains=search_param) | Q(series__description__icontains=search_param)
            )
        if category_id:
            filter_data &= (
                    Q(cinema__category_id=category_id) | Q(series__category_id=category_id)
            )
        if content_type == const_veriables.CINEMA:
            filter_data &= Q(cinema__isnull=False)
        if content_type == const_veriables.SERIES:
            filter_data &= Q(series__isnull=False)

        return super().get_queryset().filter(filter_data)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('POST', 'PATCH') or self.lookup_field in self.kwargs:
            return MyListCreateUpdateSerializerV1
        return BannerGetSerializerV1

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class BannerApiV1(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Banner.objects.select_related('cinema', 'series').order_by('-id')
    permission_classes = (IsAdmin,)
    
    def check_permissions(self, request):
        if request.method in ('POST', 'PATCH'):
            super().check_permissions(request)

    def get_queryset(self):
        params = self.request.query_params
        search_param = params.get('q')
        category_id = params.get('category_id')
        filter_data = Q()
        if search_param:
            filter_data &= (
                Q(cinema__name__icontains=search_param) | Q(cinema__description__icontains=search_param) |
                Q(series__name__icontains=search_param) | Q(series__description__icontains=search_param)
            )
        if category_id:
            filter_data &= (
                Q(cinema__category_id=category_id) | Q(series__category_id=category_id)
            )
        return super().get_queryset().filter(filter_data)

    def get_serializer_class(self):
        method = self.request.method
        if method in ('POST', 'PATCH') or self.lookup_field in self.kwargs:
            return BannerCreateUpdateSerializerV1
        return BannerGetSerializerV1

    @action(methods=['GET'], detail=False, url_name='movies', url_path='movies')
    def get_movies(self, request):
        queryset = self.get_queryset().filter(cinema__isnull=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_name='series', url_path='series')
    def get_series(self, request):
        queryset = self.get_queryset().filter(series__isnull=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SeriesApiV1(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Series.objects.select_related('genre', 'category').order_by('-id')
    permission_classes = (IsAdmin,)

    def check_permissions(self, request):
        if request.method in ('POST', 'PATCH'):
            super().check_permissions(request)

    video_param = openapi.Parameter(
        'video', in_=openapi.IN_QUERY, description='Upload video', required=False, type=openapi.TYPE_FILE
    )

    @swagger_auto_schema(manual_parameters=[video_param])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

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
    permission_classes = (IsAdmin,)

    image_param = openapi.Schema(
        'image', type=openapi.TYPE_FILE, format=openapi.FORMAT_BINARY, description='Image', required=['image']
    )

    @swagger_auto_schema(request_body=image_param)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CinemaApiV1(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Cinema.objects.select_related('genre', 'category').order_by('-id')
    permission_classes = (IsAdmin,)

    def check_permissions(self, request):
        if request.method in ('POST', 'PATCH'):
            super().check_permissions(request)

    video_param = openapi.Parameter(
        'video', in_=openapi.IN_QUERY, description='Upload video', required=False, type=openapi.TYPE_FILE
    )

    @swagger_auto_schema(manual_parameters=[video_param])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            if self.lookup_field in self.kwargs:
                return CinemaDetailReadOnlySerializerV1
            return CinemaReadOnlySerializerV1
        return CinemaWriteOnlySerializerV1


class GenreAdminApiV1(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializerV1
    permission_classes = (IsAdmin,)

    def check_permissions(self, request):
        if request.method in ('POST', 'PATCH'):
            super().check_permissions(request)

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


class CategoryAdminApiV1(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializerV1
    permission_classes = (IsAdmin,)

    def check_permissions(self, request):
        if request.method in ('POST', 'PATCH'):
            super().check_permissions(request)

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

    @action(methods=['GET'], detail=False, url_name='movies', url_path='movies')
    def get_movies(self, request):
        queryset = self.get_queryset().filter(cinema_category__isnull=False)
        serializer = CategoryListSerializerV1(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_name='series', url_path='series')
    def get_series(self, request):
        queryset = self.get_queryset().filter(series_category__isnull=False)
        serializer = CategorySeriesListSerializerV1(queryset, many=True)
        return Response(serializer.data)
