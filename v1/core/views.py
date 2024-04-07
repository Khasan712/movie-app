from drf_yasg import openapi
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from .models import Genre, Category
from .serializers import GenreSerializerV1, CategorySerializerV1
from rest_framework import mixins, viewsets
from v1.utils.permissions import IsAdmin, IsCustomer


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
