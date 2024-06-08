from django.contrib import admin
from .models import (
    Cinema, Genre, CadreCinema, Category, Series, Banner, MyList, TopCinema
)

admin.site.register(Cinema)
admin.site.register(Genre)
admin.site.register(CadreCinema)
admin.site.register(Category)
admin.site.register(Series)
admin.site.register(Banner)
admin.site.register(MyList)
admin.site.register(TopCinema)
