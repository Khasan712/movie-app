from rest_framework import serializers
from .models import Genre, Category


class GenreSerializerV1(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name')


class CategorySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

