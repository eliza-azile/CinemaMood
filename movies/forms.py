from django import forms
from .models import Genre

class MovieSelectionForm(forms.Form):
    MOOD_CHOICES = [
        ('comedy', '😄 Комедийное'),
        ('drama', '🎭 Драматическое'),
        ('adventure', '🧭 Приключенческое'),
        ('romance', '💕 Романтическое'),
        ('thriller', '🔪 Триллер'),
        ('fantasy', '🧙 Фэнтези'),
        ('action', '💥 Экшн'),
        ('sci_fi', '🚀 Научная фантастика'),
    ]
    
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
    
    selected_mood = forms.ChoiceField(
        label='Какое у вас настроение?',
        choices=MOOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    genres = forms.ModelMultipleChoiceField(
        label='Предпочитаемые жанры (необязательно)',
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'})
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