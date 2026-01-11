from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Добро пожаловать в CinemaMood!</h1><p><a href="/catalog/">Каталог</a> | <a href="/health/">Health Check</a></p>')

def catalog(request):
    return HttpResponse('<h1>Каталог фильмов</h1><p>Список всех фильмов</p>')

def movie_detail(request, movie_id):
    return HttpResponse(f'<h1>Фильм #{movie_id}</h1><p>Детальная информация о фильме</p>')

def about(request):
    return HttpResponse('<h1>О проекте</h1><p>CinemaMood - сервис для оценки фильмов</p>')

def analytics(request):
    return HttpResponse('<h1>Аналитика</h1><p>Статистика и аналитика фильмов</p>')

def history(request):
    return HttpResponse('<h1>История просмотров</h1>')

def search(request):
    return HttpResponse('<h1>Поиск фильмов</h1>')

def profile(request):
    return HttpResponse('<h1>Профиль пользователя</h1>')

def rating(request, movie_id):
    return HttpResponse(f'<h1>Рейтинг фильма #{movie_id}</h1>')

def recommendations(request):
    return HttpResponse('<h1>Рекомендации</h1>')

def favorites(request):
    return HttpResponse('<h1>Избранное</h1>')

def settings(request):
    return HttpResponse('<h1>Настройки</h1>')

def help(request):
    return HttpResponse('<h1>Помощь</h1>')

def contact(request):
    return HttpResponse('<h1>Контакты</h1>')