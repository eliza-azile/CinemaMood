import os 
import django
import sys 


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Genre 

def create_genres():
    genres_data = [
        ('comedy', 'Комедия'),
        ('drama', 'Драма'),
        ('action', 'Боевик'),
        ('fantasy', 'Фантастика'),
        ('horror', 'Ужасы'),
        ('romance', 'Мелодрама'),
        ('thriller', 'Триллер'),
        ('adventure', 'Приключение'),
        ('sci-fi', 'Научная фантастика'),
        ('animation', 'Анимация')
    ]

    created = 0
    for slug, name in genres_data:
        obj, created_flag = Genre.objects.get_or_create(
            slug=slug,
            defaults={'name': name}
        )
        if created_flag:
            created += 1
            print(f"✓ Создан жанр: {name}")
        else:
            print(f"✓ Жанр уже существует: {name}")

    print(f"\nВсего жанров в базе: {Genre.objects.count()}")
    print(f"Создано новых: {created}")

if __name__ == "__main__":
    create_genres()