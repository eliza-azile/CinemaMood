from django.urls import path, include
from . import views
from django.contrib import admin
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'CinemaMood'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('analytics/', views.analytics, name='analytics'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
]