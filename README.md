# Кинотеатр

Учебный web-проект по дисциплине, демонстрирующий кроссплатформенную работу с базой данных SQLite с использованием Python, Flask, SQLAlchemy, HTML/CSS/JavaScript и Docker.

## Описание проекта

Проект представляет собой информационную систему для кинотеатра, в которой реализованы:

- серверная часть на **Flask**
- работа с базой данных **SQLite** через ORM **SQLAlchemy**
- клиентская часть в виде web-интерфейса
- запуск в контейнерах **Docker** с помощью **docker-compose**

Приложение позволяет просматривать фильмы в прокате, расписание сеансов на сегодня, искать фильмы по жанру и просматривать топ фильмов по рейтингу.

## Цель проекта

Цель проекта — показать, как организовать:

- хранение данных в SQLite
- доступ к данным через ORM (Flask-SQLAlchemy)
- отображение данных в web-интерфейсе
- контейнеризацию backend и frontend
- совместный запуск нескольких сервисов через Docker Compose

## Структура проекта

```
lab4_cinema/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── style.css
│   └── script.js
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Назначение файлов

### Backend

- `app.py` — точка входа Flask: модели SQLAlchemy (Movie, Hall, Session), API-маршруты, создание таблиц, начальное заполнение базы данных
- `requirements.txt` — зависимости: Flask, Flask-SQLAlchemy, Flask-CORS
- `backend/Dockerfile` — сборка контейнера backend на базе Python

### Frontend

- `index.html` — основная HTML-страница: сеансы на сегодня, фильмы в прокате, поиск по жанру, топ по рейтингу
- `style.css` — стили оформления (тёмная тема с зелёным акцентом)
- `script.js` — логика загрузки данных с backend через fetch API, поиск по жанру
- `nginx.conf` — конфигурация Nginx для раздачи статических файлов
- `frontend/Dockerfile` — сборка контейнера frontend на базе Nginx

### Docker

- `docker-compose.yml` — совместный запуск frontend и backend

## Используемые технологии

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- SQLite
- HTML5
- CSS3
- JavaScript
- Docker
- Docker Compose
- Nginx

## Локальный запуск без Docker

### 1. Установить зависимости

```bash
cd backend
pip install -r requirements.txt
```

### 2. Запустить backend

```bash
cd backend
python app.py
```

Backend будет доступен по адресу:

```
http://127.0.0.1:5000
```

### 3. Запустить frontend

Во втором терминале:

```bash
cd frontend
python -m http.server 5500
```

Frontend будет доступен по адресу:

```
http://127.0.0.1:5500
```

## Запуск через Docker

### 1. Перейти в корень проекта

```bash
cd lab4_cinema
```

### 2. Собрать и запустить контейнеры

```bash
docker-compose up --build
```

### 3. Открыть в браузере

- frontend: `http://localhost:8080`
- backend: `http://localhost:5000`

### 4. Остановить контейнеры

```bash
docker-compose down
```

## API-маршруты

### Получить список фильмов

```
GET /api/movies
```

### Получить расписание на сегодня

```
GET /api/schedule
```

### Поиск фильмов по жанру

```
GET /api/search?genre=Фантастика
```

### Топ фильмов по рейтингу

```
GET /api/popular
```

## Таблицы базы данных

| Таблица | Поля |
|---------|------|
| movies | id, title, genre, rating, poster |
| halls | id, name, seats |
| sessions | id, movie_id (FK), hall_id (FK), datetime, price |

## Особенности работы с базой данных

В проекте используется SQLite — легковесная встраиваемая реляционная СУБД, которая хранит всю базу данных в одном файле и не требует отдельного сервера.

Для работы с таблицами используется ORM Flask-SQLAlchemy, которая позволяет описывать структуру базы данных через Python-классы и выполнять запросы в объектно-ориентированном стиле.

При первом запуске база данных автоматически создаётся и заполняется тестовыми данными: 8 фильмов, 3 зала, 6 сеансов.

## Автор

Студент: Дускалиев А.С

Группа: ИСИТ-31

Дисциплина: Межплатформенное программирование

Лабораторная работа №4: Кроссплатформенная работа с базами данных в Docker и через веб-интерфейс

Вариант 4: Кинотеатр
