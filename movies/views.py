from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre, UserSelection
import random

def home(request):
    """Главная страница с формой подбора"""
    
    MOOD_CHOICES = [
        ('Боевик', '🎬 Боевик / Приключения'),
        ('Комедия', '😂 Комедия'),
        ('Драма', '🎭 Драма / Мелодрама'),
        ('Фантастика', '🚀 Фантастика / Фэнтези'),
        ('Триллер', '😱 Триллер / Ужасы'),
        ('Анимация', '🧒 Анимация / Семейный'),
        ('Криминал', '🔫 Криминал / Детектив'),
    ]
    
    error_message = None
    
    if request.method == 'POST':
        selected_mood = request.POST.get('selected_mood')
        available_time = request.POST.get('available_time')
        
        if selected_mood and available_time:
            try:
                available_time = int(available_time)
                
                if available_time < 30 or available_time > 300:
                    error_message = 'Пожалуйста, введите время от 30 до 300 минут.'
                else:
                    # Маппинг настроений на английские жанры
                    mood_to_genres = {
                        'Боевик': ['action', 'adventure', 'боевик'],
                        'Комедия': ['comedy', 'комедия'],
                        'Драма': ['drama', 'romance', 'драма', 'мелодрама'],
                        'Фантастика': ['sci-fi', 'fantasy', 'фантастика', 'фэнтези'],
                        'Триллер': ['thriller', 'horror', 'триллер', 'ужасы'],
                        'Анимация': ['animation', 'cartoon', 'family', 'анимация'],
                        'Криминал': ['crime', 'detective', 'mystery', 'криминал'],
                    }
                    
                    # Находим жанры для выбранного настроения
                    genre_names = mood_to_genres.get(selected_mood, [])
                    
                    # Ищем жанры в базе (регистронезависимо)
                    from django.db.models import Q
                    query = Q()
                    for genre_name in genre_names:
                        query |= Q(name__icontains=genre_name)
                    
                    genre_objects = Genre.objects.filter(query)
                    
                    # Ищем фильмы
                    if genre_objects.exists():
                        matched_movies = Movie.objects.filter(
                            genres__in=genre_objects,
                            duration__lte=available_time
                        ).distinct().order_by('-rating')[:8]
                        
                        if matched_movies.exists():
                            # Сохраняем в сессию
                            request.session['matched_movies'] = [
                                {
                                    'id': m.id, 
                                    'title': m.title, 
                                    'poster_url': m.poster_url,
                                    'release_year': m.release_year,
                                    'rating': m.rating,
                                    'duration': m.duration,
                                    'duration_hours': m.duration_hours
                                }
                                for m in matched_movies
                            ]
                            request.session['selected_mood'] = selected_mood
                            request.session['available_time'] = available_time
                            
                            return redirect('selection_results')
                        else:
                            error_message = 'К сожалению, по вашему запросу не найдено фильмов. Попробуйте увеличить время.'
                    else:
                        error_message = f'Жанр "{selected_mood}" не найден в базе. Попробуйте другой жанр.'
                    
            except ValueError:
                error_message = 'Пожалуйста, введите корректное время (число от 30 до 300).'
        else:
            error_message = 'Пожалуйста, заполните все обязательные поля.'
    
    # Получаем случайные фильмы для блока "Сегодня в подборке"
    all_movies = list(Movie.objects.all())
    if len(all_movies) > 3:
        featured_movies = random.sample(all_movies, 3)
    elif all_movies:
        featured_movies = all_movies
    else:
        featured_movies = None
    
    context = {
        'mood_choices': MOOD_CHOICES,
        'movies_count': Movie.objects.count(),
        'genres_count': Genre.objects.count(),
        'featured_movies': featured_movies,
        'error_message': error_message,
    }
    
    return render(request, 'home.html', context)

def selection_results(request):
    """Страница результатов подбора"""
    matched_movies_data = request.session.get('matched_movies', [])
    selected_mood = request.session.get('selected_mood', 'Не выбран')
    available_time = request.session.get('available_time', 0)
    
    # Получаем полные объекты фильмов из БД
    movie_ids = [m['id'] for m in matched_movies_data]
    movies = Movie.objects.filter(id__in=movie_ids)
    
    return render(request, 'selection_results.html', {
        'movies': movies,
        'selected_mood': selected_mood,
        'available_time': available_time,
        'movies_count': len(matched_movies_data)
    })

def catalog(request):
    """Каталог всех фильмов"""
    movies = Movie.objects.all()
    
    # Фильтрация по поиску
    search = request.GET.get('search', '')
    if search:
        movies = movies.filter(title__icontains=search)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-release_year')
    if sort_by in ['title', '-title', 'release_year', '-release_year', 'rating', '-rating']:
        movies = movies.order_by(sort_by)
    
    return render(request, 'catalog.html', {
        'movies': movies[:50],
        'total_movies': movies.count()
    })

def movie_detail(request, movie_id):
    """Страница деталей фильма"""
    movie = get_object_or_404(Movie, id=movie_id)

    # Похожие фильмы (по жанрам)
    similar_movies = Movie.objects.filter(
        genres__in=movie.genres.all()
    ).exclude(id=movie.id).distinct()[:4]
    
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'similar_movies': similar_movies
    })

@login_required
def history(request):
    """История подборов пользователя"""
    user_selections = UserSelection.objects.filter(user=request.user)
    return render(request, 'history.html', {'selections': user_selections})