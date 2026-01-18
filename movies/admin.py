from django.contrib import admin
from .models import Movie, Genre, UserSelection


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'rating', 'duration_hours')
    list_filter = ('release_year', 'genres')
    search_fields = ('title', 'description')
    filter_horizontal = ('genres',)
    readonly_fields = ('duration_hours',)

    #Группировка полей в админке
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'poster_url')
        }),
        ('Детали', {
            'fields' : ('release_year', 'duration', 'rating', 'imdb_id')
        }),
        ('Жанры', {
            'fields': ('genres',)
        }),
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display=('name','slug')
    search_fields=('name',)
    prepopulated_fields={'slug': ('name',)}

@admin.register(UserSelection)
class UserSelectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'selected_mood', 'available_time', 'search_timestamp')
    list_filter = ('selected_mood', 'search_timestamp')
    filter_horizontal = ('matched_movies',)