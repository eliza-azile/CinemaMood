from django.core.management.base import BaseCommand
from movies.omdb_client import search_movies_by_title, get_movie_by_id, omdb_to_movie_data
from movies.models import Movie, Genre
import time 

class Command(BaseCommand):
    help = 'Загружает фильмы из OMDb API в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--search',
            type=str,
            default='movie',
            help='Поисковой запрос для загрузки фильмов'
        )

        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Количество фильмов для загрузки'
        )

        parser.add_argument(
            '--delay',
            type=float,
            default=1.0,
            help='Задержка между запросами в секундах (OMDb требует минимум 1 секунду для бесплатного тарифа)'
        )

    def handle(self, *args, **options):
        search_query = options['search']
        max_count = options['count']
        delay = max(options['delay'], 1.0)  # Минимум 1 секунда

        self.stdout.write(f"Ищем фильмы по запросу: '{search_query}'")

        try:
            # Шаг 1: Ищем фильмы по названию
            search_results = search_movies_by_title(search_query)

            if not search_results:
                self.stdout.write(self.style.ERROR("Не найдено фильмов по запросу"))
                return
            
            created_count = 0
            skipped_count = 0

            # Шаг 2: Для каждого найденного фильма получаем детали
            for i, result in enumerate(search_results[:max_count]):
                time.sleep(delay)  # Соблюдаем лимиты API

                imdb_id = result.get('imdbID')
                if not imdb_id:
                    continue
                
                # Проверяем, есть ли уже фильм с таким IMDb ID
                if Movie.objects.filter(imdb_id=imdb_id).exists():
                    self.stdout.write(f"Фильм '{result.get('Title')}' уже существует, пропускаем")
                    skipped_count += 1
                    continue

                # Получаем детальную информацию
                try:
                    details = get_movie_by_id(imdb_id)

                    if details.get('Response') != 'True':
                        self.stdout.write(f"Не удалось получить детали для {imdb_id}")
                        continue

                    # Преобразуем данные
                    movie_data = omdb_to_movie_data(details)
                    movie_data['imdb_id'] = imdb_id

                    # Создаем фильм
                    movie = Movie.objects.create(**movie_data)

                    # OMDb возвращает жанры как строка "Action, Drama, Sci-Fi"
                    genres_str = details.get('Genre', '')
                    if genres_str and genres_str != 'N/A':
                        for genre_name in genres_str.split(','):
                            genre_name = genre_name.strip().lower()
                            if genre_name:
                                genre, _ = Genre.objects.get_or_create(name=genre_name)
                                movie.genres.add(genre)

                    created_count += 1
                    self.stdout.write(f"[{created_count}] ✓ Добавлен: {movie.title}")

                except Exception as e:
                    self.stdout.write(f"Ошибка при загрузке {result.get('Title')}: {e}")
                    continue
            
            # Сообщаем об итогах
            self.stdout.write(
                self.style.SUCCESS(
                    f"Загрузка завершена! Создано: {created_count}, Пропущено: {skipped_count}"
                ) 
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))