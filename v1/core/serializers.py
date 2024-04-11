from rest_framework import serializers
from .models import Genre, Category, Cinema, Series, CadreCinema
from ..utils.raise_errors import SerializerRaise400


class SeriesDetailReadOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = (
            'id', 'genre', 'category', 'main_image', 'trailer', 'trailer_url', 'name', 'year', 'description', 'rejisor',
            'main_users', 'video'
        )

    def to_representation(self, instance):
        res = super().to_representation(instance)
        cadre = CadreCinema.objects.select_related('series').filter(series_id=instance.id)
        res['cadre'] = CinemaCadreSerializerV1(cadre, many=True).data
        genre = res.get('genre')
        if genre:
            res['genre'] = GenreSerializerV1(instance.genre).data
        category = res.get('category')
        if category:
            res['category'] = CategorySerializerV1(instance.category).data
        if not instance.parent:
            series = Series.objects.filter(parent_id=instance.id)
            res['series_qty'] = series.count()
            res['series'] = self.__class__(series, many=True).data
        return res


class SeriesReadOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ('id', 'genre', 'category', 'main_image', 'name', 'year', 'description')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        genre = res.get('genre')
        if genre:
            res['genre'] = GenreSerializerV1(instance.genre).data
        category = res.get('category')
        if category:
            res['category'] = CategorySerializerV1(instance.category).data
        if not instance.parent:
            res['series_qty'] = Series.objects.filter(parent_id=instance.id).count()
        return res


class SeriesWriteOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = (
            'id', 'genre', 'category', 'main_image', 'trailer', 'trailer_url', 'name', 'year', 'description', 'rejisor',
            'main_users', 'video', 'parent'
        )

    def to_representation(self, instance):
        return {
            "success": True,
            'id': instance.id
        }


class CadreCreateSerializerV1(serializers.Serializer):
    cinema_id = serializers.IntegerField(required=False)
    series_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        cinema_id = validated_data.get('cinema_id')
        series_id = validated_data.get('series_id')

        if cinema_id:
            cadre_list = []
            images = self.context['request'].FILES.getlist('image')
            if not images:
                raise SerializerRaise400({'error': 'Upload image!'})
            for image in images:
                cadre_list.append(CadreCinema(
                    cinema_id=cinema_id, image=image
                ))
            CadreCinema.objects.bulk_create(cadre_list)
            return validated_data

        elif series_id:
            cadre_list = []
            images = self.context['request'].FILES.getlist('image')
            if not images:
                raise SerializerRaise400({'error': 'Upload image!'})
            for image in images:
                cadre_list.append(CadreCinema(
                    series_id=series_id, image=image
                ))
            CadreCinema.objects.bulk_create(cadre_list)
            return validated_data
        else:
            raise SerializerRaise400({"error": 'Choose cinema or series!!!'})

    def to_representation(self, instance):
        return {
            "success": True
        }


class CinemaCadreSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = CadreCinema
        fields = ('id', 'image')


class CinemaDetailReadOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = (
            'id', 'genre', 'category', 'main_image', 'trailer', 'trailer_url', 'name', 'year', 'description', 'rejisor',
            'main_users', 'video'
        )

    def to_representation(self, instance):
        res = super().to_representation(instance)
        cadre = CadreCinema.objects.select_related('cinema').filter(cinema_id=instance.id)
        res['cadre'] = CinemaCadreSerializerV1(cadre, many=True).data
        genre = res.get('genre')
        if genre:
            res['genre'] = GenreSerializerV1(instance.genre).data
        category = res.get('category')
        if category:
            res['category'] = CategorySerializerV1(instance.category).data
        return res


class CinemaReadOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ('id', 'genre', 'category', 'main_image', 'name', 'year', 'description')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        genre = res.get('genre')
        if genre:
            res['genre'] = GenreSerializerV1(instance.genre).data
        category = res.get('category')
        if category:
            res['category'] = CategorySerializerV1(instance.category).data
        return res


class CinemaWriteOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = (
            'id', 'genre', 'category', 'main_image', 'trailer', 'trailer_url', 'name', 'year', 'description', 'rejisor',
            'main_users', 'video'
        )

    def to_representation(self, instance):
        return {
            "success": True,
            'id': instance.id
        }


class GenreSerializerV1(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name')


class CategorySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

