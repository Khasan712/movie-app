from django.db import models
from v1.utils.abstract import CustomBaseAbstract
from v1.users.models import User


class Genre(CustomBaseAbstract):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_uz


class Category(CustomBaseAbstract):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_uz


class Cinema(CustomBaseAbstract):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='cinema_category'
    )
    main_image = models.ImageField(upload_to='cinema/main_image/')
    trailer = models.FileField(upload_to='cinema/trailer/', blank=True, null=True)
    trailer_url = models.CharField(max_length=500, blank=True, null=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    description_uz = models.CharField(max_length=500, blank=True, null=True)
    description_ru = models.CharField(max_length=255, blank=True, null=True)
    description_en = models.CharField(max_length=255, blank=True, null=True)
    rejisor = models.CharField(max_length=255, blank=True, null=True)
    main_users = models.CharField(max_length=500, blank=True, null=True)
    video = models.FileField(upload_to='cinema/video/', blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name_uz}'


class Series(CustomBaseAbstract):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='series_category'
    )
    main_image = models.ImageField(upload_to='series/main_image/')
    trailer = models.FileField(upload_to='series/trailer/', blank=True, null=True)
    trailer_url = models.CharField(max_length=500, blank=True, null=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    description_uz = models.CharField(max_length=500, blank=True, null=True)
    description_ru = models.CharField(max_length=255, blank=True, null=True)
    description_en = models.CharField(max_length=255, blank=True, null=True)
    rejisor = models.CharField(max_length=255, blank=True, null=True)
    main_users = models.CharField(max_length=500, blank=True, null=True)
    video = models.FileField(upload_to='series/video/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name_uz}'


class CadreCinema(CustomBaseAbstract):
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='cinema/cadre/')

    def __str__(self):
        return f'{self.id}'


class Banner(CustomBaseAbstract):
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'


class MyList(CustomBaseAbstract):
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('cinema', 'user'), ('series', 'user'))

    def __str__(self):
        return f'{self.id}'


class TopCinema(CustomBaseAbstract):
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'
