from django import forms
from .models import Genre, Movie

class MovieSelectionForm(forms.Form):
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


class MovieSearchForm(forms.Form):
    search_query = forms.CharField(
        label='Поиск фильмов',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название фильма, режиссер, год...'
        })
    )


class CatalogFilterForm(forms.Form):
    """Форма фильтрации в каталоге"""
    
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        label='Жанр',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Все жанры"
    )
    
    min_year = forms.IntegerField(
        label='Год от',
        min_value=1900,
        max_value=2024,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': '1900'
        })
    )
    
    max_year = forms.IntegerField(
        label='Год до',
        min_value=1900,
        max_value=2024,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': '2024'
        })
    )
    
    min_rating = forms.FloatField(
        label='Рейтинг от',
        min_value=0.0,
        max_value=10.0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.0',
            'step': '0.1'
        })
    )
    
    SORT_CHOICES = [
        ('-rating', 'Рейтинг (высокий → низкий)'),
        ('rating', 'Рейтинг (низкий → высокий)'),
        ('-release_year', 'Год (новые → старые)'),
        ('release_year', 'Год (старые → новые)'),
        ('title', 'Название (А-Я)'),
        ('-title', 'Название (Я-А)'),
        ('duration', 'Длительность (короткие → длинные)'),
        ('-duration', 'Длительность (длинные → короткие)'),
    ]
    
    sort_by = forms.ChoiceField(
        label='Сортировка',
        choices=SORT_CHOICES,
        required=False,
        initial='-rating',
        widget=forms.Select(attrs={'class': 'form-control'})
    )