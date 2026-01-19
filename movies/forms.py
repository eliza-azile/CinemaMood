from django import forms
from .models import Genre, Movie


class MovieSelectionForm(forms.Form):
    MOOD_CHOICES = [
        ('', 'Выберите настроение...'),
        ('Боевик', '🎬 Боевик / Приключения'),
        ('Комедия', '😂 Комедия'),
        ('Драма', '🎭 Драма / Мелодрама'),
        ('Фантастика', '🚀 Фантастика / Фэнтези'),
        ('Триллер', '😱 Триллер / Ужасы'),
        ('Анимация', '🧒 Анимация / Семейный'),
        ('Криминал', '🔫 Криминал / Детектив'),
    ]
    
    selected_mood = forms.ChoiceField(
        choices=MOOD_CHOICES,
        label='Какое у вас настроение?',
        widget=forms.Select(attrs={'class': 'form-control form-select-lg'})
    )
    
    available_time = forms.IntegerField(
        label='Сколько времени у вас есть? (минут)',
        min_value=30,
        max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '120'
        }),
        initial=120
    )
    """Форма для подбора фильмов по настроению и времени"""
    
    selected_genre = forms.ModelChoiceField(
        queryset=Genre.objects.all().order_by('name'),
        label='Какое у вас настроение/жанр?',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выберите жанр...",
        help_text="Выберите жанр, который соответствует вашему настроению"
    )
    
    available_time = forms.IntegerField(
        label='Сколько времени у вас есть? (минут)',
        min_value=30,
        max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например, 120'
        }),
        help_text='От 30 до 300 минут'
    )
    
    min_rating = forms.FloatField(
        label='Минимальный рейтинг (необязательно)',
        min_value=0.0,
        max_value=10.0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например, 7.0',
            'step': '0.1'
        }),
        initial=6.0,
        help_text="Фильмы с рейтингом ниже не будут показаны"
    )

    max_duration = forms.IntegerField(
        label='Максимальная длительность (необязательно)',
        min_value=30,
        max_value=300,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например, 150'
        }),
        help_text="Если оставить пустым, будет использовано доступное время"
    )