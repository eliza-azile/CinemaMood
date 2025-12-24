from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('analytics/', views.analytics, name='analytics'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
]