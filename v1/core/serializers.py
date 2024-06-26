from rest_framework import serializers
from .models import Genre, Category, Cinema, Series, CadreCinema, Banner, MyList, TopCinema
from ..services.google_translate import google_translate_text
from ..utils.const_veriables import EN_LANG, RU_LANG
from ..utils.raise_errors import SerializerRaise400


class SeriesLessDataSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ('id', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'main_image')


class CategorySeriesListSerializerV1(serializers.Serializer):

    def to_representation(self, instance):
        series = Series.objects.filter(category_id=instance.id, parent_id=None).order_by('-id')[:5]
        return {
            'id': instance.id,
            'name_uz': instance.name_uz,
            'name_ru': instance.name_ru,
            'name_en': instance.name_en,
            'Series': SeriesLessDataSerializerV1(series, many=True).data
        }


class CinemaLessDataSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = (
            'id', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'main_image'
        )


class CategoryListSerializerV1(serializers.Serializer):

    def to_representation(self, instance):
        movies = Cinema.objects.filter(category_id=instance.id).order_by('-id')[:5]
        return {
            'id': instance.id,
            'name_uz': instance.name_uz,
            'name_ru': instance.name_ru,
            'name_en': instance.name_en,
            'movies': CinemaLessDataSerializerV1(movies, many=True).data
        }


class BannerGetSerializerV1(serializers.Serializer):

    def to_representation(self, instance):
        if instance.cinema:
            is_in_my_list = MyList.objects.select_related('cinema', 'user').filter(
                cinema_id=instance.cinema.id, user_id=self.context['request'].user.id
            ).first()
            return {
                'id': instance.id,
                'movie': CinemaLessDataSerializerV1(instance.cinema).data,
                'is_in_my_list': True if is_in_my_list else False
            }

        is_in_my_list = MyList.objects.select_related('series', 'user').filter(
            series_id=instance.series.id, user_id=self.context['request'].user.id
        ).first()
        return {
            'id': instance.id,
            'series': SeriesLessDataSerializerV1(instance.series).data,
            'is_in_my_list': True if is_in_my_list else False
        }


class BannerCreateUpdateSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'cinema', 'series')

    def create(self, validated_data):
        obj = Banner.objects.filter(**validated_data).first()
        if obj:
            raise SerializerRaise400({'error': 'Already exists'})
        return super().create(validated_data)

    def to_representation(self, instance):
        return BannerGetSerializerV1(instance, context=self.context).data


class TopCinemaCreateUpdateSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = TopCinema
        fields = ('id', 'cinema', 'series')

    def to_representation(self, instance):
        return BannerGetSerializerV1(instance).data


class MyListCreateUpdateSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = MyList
        fields = ('id', 'cinema', 'series')

    def to_representation(self, instance):
        return BannerGetSerializerV1(instance).data


class SeriesDetailReadOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = (
            'id', 'genre', 'category', 'main_image', 'trailer', 'trailer_url', 'name_uz', 'name_ru', 'name_en', 'year',
            'description_uz', 'description_ru', 'description_en', 'rejisor', 'main_users', 'video'
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
            is_in_my_list = MyList.objects.select_related('series', 'user').filter(
                series_id=instance.id, user_id=self.context['request'].user.id
            ).first()
            res['is_in_my_list'] = True if is_in_my_list else False
        else:
            is_in_my_list = MyList.objects.select_related('series', 'user').filter(
                series_id=instance.parent.id, user_id=self.context['request'].user.id
            ).first()
            res['is_in_my_list'] = True if is_in_my_list else False
        return res


class SeriesReadOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = (
            'id', 'genre', 'category', 'main_image', 'name_uz', 'name_ru', 'name_en', 'year', 'description_uz',
            'description_ru', 'description_en'
        )

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
            'id', 'genre', 'category', 'main_image', 'trailer', 'trailer_url', 'name_uz', 'name_ru', 'name_en', 'year',
            'description_uz', 'description_ru', 'description_en', 'rejisor', 'main_users', 'video', 'parent'
        )
        extra_kwargs = {
            'name_ru': {'read_only': True},
            'name_en': {'read_only': True},
            'description_ru': {'read_only': True},
            'description_en': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['name_en'] = google_translate_text(EN_LANG, validated_data['name_uz'])
        validated_data['name_ru'] = google_translate_text(RU_LANG, validated_data['name_uz'])
        if validated_data.get('description_uz'):
            validated_data['description_en'] = google_translate_text(EN_LANG, validated_data['description_uz'])
            validated_data['description_ru'] = google_translate_text(RU_LANG, validated_data['description_uz'])
        return super().create(validated_data)

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
            'id', 'genre', 'category', 'main_image', 'trailer', 'trailer_url', 'name_uz', 'name_ru', 'name_en', 'year',
            'description_uz', 'description_ru', 'description_en', 'rejisor', 'main_users', 'video'
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
        is_in_my_list = MyList.objects.select_related('cinema', 'user').filter(
            cinema_id=instance.id, user_id=self.context['request'].user.id
        ).first()
        res['is_in_my_list'] = True if is_in_my_list else False
        return res


class CinemaReadOnlySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = (
            'id', 'genre', 'category', 'main_image', 'name_uz', 'name_ru', 'name_en', 'year', 'description_uz',
            'description_ru', 'description_en'
        )

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
            'id', 'genre', 'category', 'main_image', 'trailer', 'trailer_url', 'name_uz', 'name_ru', 'name_en', 'year',
            'description_uz', 'description_ru', 'description_en', 'rejisor', 'main_users', 'video'
        )
        extra_kwargs = {
            'name_ru': {'read_only': True},
            'name_en': {'read_only': True},
            'description_ru': {'read_only': True},
            'description_en': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['name_en'] = google_translate_text(EN_LANG, validated_data['name_uz'])
        validated_data['name_ru'] = google_translate_text(RU_LANG, validated_data['name_uz'])
        if validated_data.get('description_uz'):
            validated_data['description_en'] = google_translate_text(EN_LANG, validated_data['description_uz'])
            validated_data['description_ru'] = google_translate_text(RU_LANG, validated_data['description_uz'])
        return super().create(validated_data)

    def to_representation(self, instance):
        return {
            "success": True,
            'id': instance.id
        }


class GenreSerializerV1(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name_uz', 'name_ru', 'name_en')
        extra_kwargs = {
            'name_ru': {'read_only': True},
            'name_en': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['name_en'] = google_translate_text(EN_LANG, validated_data['name_uz'])
        validated_data['name_ru'] = google_translate_text(RU_LANG, validated_data['name_uz'])
        return super().create(validated_data)


class CategorySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name_uz', 'name_ru', 'name_en')
        extra_kwargs = {
            'name_ru': {'read_only': True},
            'name_en': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['name_en'] = google_translate_text(EN_LANG, validated_data['name_uz'])
        validated_data['name_ru'] = google_translate_text(RU_LANG, validated_data['name_uz'])
        return super().create(validated_data)

