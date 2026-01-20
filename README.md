CinemaMood 
Подбор фильмов по настроению и доступному времени


🌟 О проекте

CinemaMood — это умный веб-сервис для подбора фильмов, который анализирует ваше текущее настроение и доступное время для просмотра. Больше не нужно тратить полчаса на выбор фильма!

Демо: [cinemamood.onrender.com](https://cinemamood.onrender.com)

✨ Особенности

- 🎯 Подбор по времени — укажите, сколько минут у вас есть, и система подберет фильмы, которые точно поместятся
- 😊 Подбор по настроению — выберите жанр, соответствующий вашему эмоциональному состоянию
- 📊 Персонализация — авторизованные пользователи сохраняют историю подборов
- 🎬 Богатая база — интеграция с OMDb API, тысячи фильмов с описаниями и постерам


🛠️ Технологический стек

 Backend
- Python 3.11 — основной язык программирования
- Django 4.2 — веб-фреймворк
- Django ORM — работа с базой данных
- SQLite (разработка) / PostgreSQL (продакшн)

 Frontend
- HTML5/CSS3 — разметка и стили
- Bootstrap 5.3 — адаптивный дизайн
- JavaScript — интерактивные элементы

 API и интеграции
- OMDb API — база данных фильмов
- Django REST Framework (опционально для будущего API)

 Инструменты
- Git — контроль версий
- Render — облачный хостинг


📦 Установка и запуск

 1. Клонирование репозитория
```bash
git clone https://github.com/eliza-azile/CinemaMood.git
cd CinemaMood
```

 2. Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

 4. Настройка переменных окружения
Создайте файл `.env` в корне проекта:
```env
DEBUG=True
SECRET_KEY=ваш_секретный_ключ
OMDB_API_KEY=ваш_ключ_от_omdbapi.com
DATABASE_URL=sqlite:///db.sqlite3
```

Как получить OMDb API ключ:
1. Зарегистрируйтесь на [omdbapi.com](https://www.omdbapi.com/apikey.aspx)
2. Выберите бесплатный тариф (1000 запросов в день)
3. Скопируйте ключ в `.env`

 5. Применение миграций и загрузка данных
```bash
python manage.py migrate
python manage.py load_movies_from_omdb --search="action" --count=5
python manage.py load_movies_from_omdb --search="comedy" --count=5
python manage.py createsuperuser  # для доступа к админке
```

 6. Запуск сервера
```bash
python manage.py runserver
```
Откройте в браузере: [http://127.0.0.1:8000](http://127.0.0.1:8000)

 🚀 Деплой на Render

Проект автоматически деплоится на Render при пуше в ветку `main`.

Спецификации на Render:
- Instance Type: Free
- Python Version: 3.11
- Build Command: 
  ```bash
  pip install -r requirements.txt &&  python manage.py migrate &&  python manage.py load_movies_from_omdb --search="action" --count=3 && python manage.py load_movies_from_omdb --search="comedy" --count=3 && python manage.py load_movies_from_omdb --search="drama" --count=3 && python manage.py load_movies_from_omdb --search="sci-fi" --count=3 && python manage.py load_movies_from_omdb --search="horror" --count=3 && python manage.py load_movies_from_omdb --search="animation" --count=3 && python manage.py load_movies_from_omdb --search="crime" --count=3 && python manage.py load_movies_from_omdb --search="adventure" --count=3 && python manage.py load_movies_from_omdb --search="fantasy" --count=3 && python manage.py load_movies_from_omdb --search="thriller" --count=3
  ```
- Start Command: 
  ```bash
  python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2
  ```

📁 Структура проекта

CinemaMood/
├── config/                # Настройки Django
├── movies/                # Основное приложение
│   ├── models.py          # Модели: Movie, Genre, UserSelection
│   ├── views.py           # Контроллеры
│   ├── urls.py            # Маршруты
│   └── templates/         # HTML шаблоны
├── templates/             # Базовые шаблоны
├── static/                # Статические файлы
├── scripts/               # Вспомогательные скрипты
├── requirements.txt       # Зависимости Python
├── manage.py             # Django CLI
└── README.md             # Эта документация


 👥 Роли пользователей

Гость : Подбор фильмов по времени и настроению, просмотр каталога
Авторизованный пользователь : Все возможности гостя + сохранение истории подборов
Администратор : Полный доступ к админ-панели Django


 🔧 Команды для разработки

```bash
# Загрузить фильмы определенного жанра
python manage.py load_movies_from_omdb --search="drama" --count=10

# Создать резервную копию данных
python manage.py dumpdata movies > fixtures/movies.json

# Загрузить данные из фикстур
python manage.py loaddata fixtures/movies.json

# Запустить тесты
python manage.py test

# Проверить покрытие кода тестами
coverage run manage.py test && coverage report
```

 📊 Модели данных

# Основные модели:
1. Movie - Фильм (название, описание, длительность, год, рейтинг)
2. Genre - Жанр (название, slug)
3. UserSelection - История подбора пользователя


 🤝 Как внести вклад

1. Форкните репозиторий
2. Создайте ветку для новой функциональности:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Внесите изменения и сделайте коммит:
   ```bash
   git commit -m "feat: add new feature"
   ```
4. Отправьте изменения:
   ```bash
   git push origin feature/new-feature
   ```
5. Создайте Pull Request


## 👏 Благодарности

- [OMDb API](https://www.omdbapi.com/) за данные о фильмах
- [Django](https://www.djangoproject.com/) за отличный фреймворк
- [Bootstrap](https://getbootstrap.com/) за стили
- [Render](https://render.com) за бесплатный хостинг

## 📞 Контакты

Автор: Eliza Kolokoltsova  
GitHub: [@eliza-azile](https://github.com/eliza-azile)  
Проект: [CinemaMood Repository](https://github.com/eliza-azile/CinemaMood)

---
Если вам понравился проект, поставьте ⭐ на GitHub
