from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('selection-results/', views.selection_results, name='selection_results'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('history/', views.history, name='history'),

]