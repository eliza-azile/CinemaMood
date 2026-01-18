from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    """Настроение или жанровый тег для фильма"""
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Жанр"
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True,
        verbose_name="URL-идентификатор"
    )
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']
        db_table = 'movies_genre'
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    """Фильм в базе данных"""
    title = models.CharField(
        max_length=225,
        verbose_name="Название фильма"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    duration = models.PositiveIntegerField(
        verbose_name="Длительность (в минутах)",
        help_text="Сколько минут длится фильм"
    )
    release_year = models.PositiveIntegerField(
        verbose_name="Год выпуска"
    )
    rating = models.FloatField(
        default=0.0,
        verbose_name="Рейтинг",
        help_text="От 0.0 до 10.0",
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    poster_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на постер"
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='movies',
        verbose_name="Жанры",
        help_text="К каким жанрам относится фильм"
    )
    imdb_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="IMDb ID"
    )
    
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ['-release_year', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    @property
    def duration_hours(self):
        """Возвращает длительность в формате '2 ч 15 мин'"""
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours > 0:
            return f"{hours} ч {minutes} мин"
        return f"{minutes} мин"

class UserSelection(models.Model):
    """История подбора фильмов пользователем"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Пользователь"
    )
    selected_mood = models.CharField(
        max_length=100,
        verbose_name="Выбранное настроение"
    )
    available_time = models.IntegerField(
        verbose_name="Доступное время (минуты)"
    )
    search_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время поиска"
    )
    matched_movies = models.ManyToManyField(
        Movie,
        verbose_name="Подобранные фильмы"
    )
    
    class Meta:
        verbose_name = "История подбора"
        verbose_name_plural = "Истории подборов"
        ordering = ['-search_timestamp']
    
    def __str__(self):
        return f"Подбор от {self.search_timestamp.strftime('%d.%m.%Y %H:%M')}"