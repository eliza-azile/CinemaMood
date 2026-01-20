from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('selection-results/', views.selection_results, name='selection_results'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('history/', views.history, name='history'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),
    
    path('register/', views.register, name='register'),
]