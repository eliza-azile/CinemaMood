import requests
from django.conf import settings
from .models import Movie, Genre

def get_omdb_data(params):
    """
    Базовый метод для запросов к OMDb API
    """
    params['apikey'] = settings.OMDB_API_KEY
    response = requests.get(settings.OMDB_BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def search_movies_by_title(title):
    """
    Поиск фильмов по названию
    Возвращает список фильмов
    """
    data = get_omdb_data({"s": title, "type": "movie"})
    return data.get('Search', []) if data.get('Response') == 'True' else []

def get_movie_by_id(imdb_id):
    """
    Получение детальной информации по IMDb ID
    """
    return get_omdb_data({"i": imdb_id, "plot": "full"})

def get_movie_by_title(title):
    """
    Получение детальной информации по названию
    """
    return get_omdb_data({"t": title, "plot": "full"})

def omdb_to_movie_data(omdb_movie):
    """
    Преобразование данных OMDb в формат для нашей модели Movie
    """
    # Конвертируем время из строки "142 min" в число
    duration = 0
    if 'Runtime' in omdb_movie and omdb_movie['Runtime'] != 'N/A':
        try:
            duration = int(omdb_movie['Runtime'].split()[0])
        except:
            pass
    
    # Конвертируем рейтинг
    rating = 0.0
    if 'imdbRating' in omdb_movie and omdb_movie['imdbRating'] != 'N/A':
        try:
            rating = float(omdb_movie['imdbRating'])
        except:
            pass
    
    # Получаем год
    release_year = None
    if 'Year' in omdb_movie and omdb_movie['Year'] != 'N/A':
        try:
            # Может быть "2020-2022" для сериалов, берем первую часть
            release_year = int(omdb_movie['Year'].split('-')[0])
        except:
            pass
    
    return {
        'title': omdb_movie.get('Title', ''),
        'description': omdb_movie.get('Plot', ''),
        'duration': duration,
        'release_year': release_year,
        'rating': rating,
        'poster_url': omdb_movie.get('Poster', ''),
        'imdb_id': omdb_movie.get('imdbID'),  # сохраняем IMDb ID
    }