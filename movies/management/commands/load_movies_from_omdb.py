from django.core.management.base import BaseCommand
from movies.omdb_client import search_movies_by_title, get_movie_by_id, omdb_to_movie_data
from movies.models import Movie, Genre
import time 
import hashlib

class Command(BaseCommand):
    help = 'Загружает фильмы из OMDb API в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--search',
            type=str,
            default='action',
            help='Поисковой запрос для загрузки фильмов'
        )

        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Количество фильмов для загрузки'
        )

    def handle(self, *args, **options):
        search_query = options['search']
        max_count = options['count']

        self.stdout.write(f"Ищем фильмы по запросу: '{search_query}'")

        try:
            # Шаг 1: Ищем фильмы по названию
            search_results = search_movies_by_title(search_query)

            if not search_results:
                self.stdout.write(self.style.ERROR("Не найдено фильмов по запросу"))
                return
            
            created_count = 0

            # Шаг 2: Для каждого найденного фильма получаем детали
            for i, result in enumerate(search_results[:max_count]):
                time.sleep(1.0)  # Соблюдаем лимиты API

                imdb_id = result.get('imdbID')
                if not imdb_id:
                    continue
                
                # Проверяем по названию и году
                title = result.get('Title')
                year_str = result.get('Year', '').split('-')[0]

                if title and year_str and year_str.isdigit():
                    year = int(year_str)
                    if Movie.objects.filter(title=title, release_year=year).exists():
                        self.stdout.write(f"Фильм '{title}' ({year}) уже существует, пропускаем")
                        continue

                # Получаем детальную информацию
                try:
                    details = get_movie_by_id(imdb_id)

                    if details.get('Response') != 'True':
                        self.stdout.write(f"Не удалось получить детали для {imdb_id}")
                        continue

                    # Преобразуем данные
                    movie_data = omdb_to_movie_data(details)
                    
                    # Убираем imdb_id из данных
                    if 'imdb_id' in movie_data:
                        del movie_data['imdb_id']
                    
                    # Создаем фильм
                    movie = Movie.objects.create(**movie_data)

                    # Обрабатываем жанры с уникальными slug
                    genres_str = details.get('Genre', '')
                    if genres_str and genres_str != 'N/A':
                        genre_list = [g.strip() for g in genres_str.split(',') if g.strip()]
                        
                        for genre_name in genre_list:
                            # Создаем более уникальный slug
                            slug_base = genre_name.lower().replace(' ', '-').replace('&', 'and')
                            slug = slug_base
                            
                            # Проверяем, существует ли уже slug
                            counter = 1
                            while Genre.objects.filter(slug=slug).exists():
                                slug = f"{slug_base}-{counter}"
                                counter += 1
                            
                            genre, created = Genre.objects.get_or_create(
                                name=genre_name,
                                defaults={'slug': slug}
                            )
                            
                            if created:
                                self.stdout.write(f"  Создан жанр: {genre_name} (slug: {slug})")
                            
                            movie.genres.add(genre)

                    created_count += 1
                    self.stdout.write(f"[{created_count}] ✓ Добавлен: {movie.title} ({movie.release_year})")

                except Exception as e:
                    self.stdout.write(f"Ошибка при загрузке {result.get('Title')}: {str(e)[:100]}")
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(f"Загрузка завершена! Создано: {created_count} фильмов")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))