#!/usr/bin/env python3
"""
Лабораторная работа №4 — Кинотеатр
Docker + Flask + SQLAlchemy + SQLite
"""

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cinema.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ==================== МОДЕЛИ ====================
class Movie(db.Model):
    __tablename__ = "movies"
    id       = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(120), nullable=False)
    genre    = db.Column(db.String(60), nullable=False)
    rating   = db.Column(db.Float, default=0.0)
    sessions = db.relationship("Session", backref="movie", lazy=True, cascade="all, delete-orphan")

class Hall(db.Model):
    __tablename__ = "halls"
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(60), nullable=False)
    seats   = db.Column(db.Integer, default=50)
    sessions = db.relationship("Session", backref="hall", lazy=True, cascade="all, delete-orphan")

class Session(db.Model):
    __tablename__ = "sessions"
    id        = db.Column(db.Integer, primary_key=True)
    movie_id  = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    hall_id   = db.Column(db.Integer, db.ForeignKey("halls.id"), nullable=False)
    datetime  = db.Column(db.DateTime, nullable=False)
    price     = db.Column(db.Float, default=300.0)

# ==================== СТРАНИЦЫ ====================
@app.route("/")
def index():
    return render_template("index.html")

# ==================== API ====================

# --- Фильмы ---
@app.route("/api/movies", methods=["GET", "POST"])
def api_movies():
    if request.method == "POST":
        data = request.json
        m = Movie(title=data["title"], genre=data["genre"], rating=data.get("rating", 0))
        db.session.add(m)
        db.session.commit()
        return jsonify({"id": m.id, "title": m.title, "genre": m.genre, "rating": m.rating}), 201

    movies = Movie.query.all()
    return jsonify([{"id": m.id, "title": m.title, "genre": m.genre, "rating": m.rating} for m in movies])

@app.route("/api/movies/<int:id>", methods=["DELETE"])
def api_movie_delete(id):
    m = Movie.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({"ok": True})

# --- Залы ---
@app.route("/api/halls", methods=["GET", "POST"])
def api_halls():
    if request.method == "POST":
        data = request.json
        h = Hall(name=data["name"], seats=data.get("seats", 50))
        db.session.add(h)
        db.session.commit()
        return jsonify({"id": h.id, "name": h.name, "seats": h.seats}), 201

    halls = Hall.query.all()
    return jsonify([{"id": h.id, "name": h.name, "seats": h.seats} for h in halls])

# --- Сеансы ---
@app.route("/api/sessions", methods=["GET", "POST"])
def api_sessions():
    if request.method == "POST":
        data = request.json
        s = Session(
            movie_id=data["movie_id"],
            hall_id=data["hall_id"],
            datetime=datetime.fromisoformat(data["datetime"]),
            price=data.get("price", 300)
        )
        db.session.add(s)
        db.session.commit()
        return jsonify({"id": s.id, "movie_id": s.movie_id, "hall_id": s.hall_id,
                        "datetime": s.datetime.isoformat(), "price": s.price}), 201

    sessions = Session.query.order_by(Session.datetime).all()
    result = []
    for s in sessions:
        result.append({
            "id": s.id,
            "movie": s.movie.title,
            "hall": s.hall.name,
            "datetime": s.datetime.strftime("%d.%m.%Y %H:%M"),
            "price": s.price
        })
    return jsonify(result)

@app.route("/api/sessions/<int:id>", methods=["DELETE"])
def api_session_delete(id):
    s = Session.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"ok": True})

# --- Запросы ---
@app.route("/api/schedule")
def api_schedule():
    """Расписание на сегодня"""
    today = datetime.today().strftime("%Y-%m-%d")
    sessions = Session.query.filter(Session.datetime.like(f"{today}%")).order_by(Session.datetime).all()
    result = []
    for s in sessions:
        result.append({
            "movie": s.movie.title,
            "hall": s.hall.name,
            "time": s.datetime.strftime("%H:%M"),
            "price": s.price
        })
    return jsonify(result)

@app.route("/api/search_by_genre")
def api_search_by_genre():
    """Поиск фильмов по жанру"""
    genre = request.args.get("genre", "")
    movies = Movie.query.filter(Movie.genre.ilike(f"%{genre}%")).all()
    return jsonify([{"title": m.title, "genre": m.genre, "rating": m.rating} for m in movies])

@app.route("/api/popular")
def api_popular():
    """Самые популярные фильмы (по рейтингу)"""
    movies = Movie.query.order_by(Movie.rating.desc()).limit(5).all()
    return jsonify([{"title": m.title, "genre": m.genre, "rating": m.rating} for m in movies])

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Заполнение тестовыми данными (если пусто)
        if not Movie.query.first():
            db.session.add_all([
                Movie(title="Дюна 2", genre="Фантастика", rating=8.5),
                Movie(title="Оппенгеймер", genre="Драма", rating=8.9),
                Movie(title="Джон Уик 4", genre="Боевик", rating=7.8),
                Movie(title="Барби", genre="Комедия", rating=6.9),
                Movie(title="Человек-паук", genre="Фантастика", rating=8.2),
            ])
            db.session.add_all([
                Hall(name="Зал 1", seats=100),
                Hall(name="Зал 2", seats=80),
                Hall(name="Зал 3", seats=60),
            ])
            db.session.commit()

            m = Movie.query.all()
            h = Hall.query.all()
            db.session.add_all([
                Session(movie_id=m[0].id, hall_id=h[0].id, datetime=datetime(2026,5,5,10,0), price=350),
                Session(movie_id=m[1].id, hall_id=h[1].id, datetime=datetime(2026,5,5,13,0), price=400),
                Session(movie_id=m[2].id, hall_id=h[2].id, datetime=datetime(2026,5,5,16,0), price=300),
                Session(movie_id=m[3].id, hall_id=h[0].id, datetime=datetime(2026,5,5,19,0), price=250),
                Session(movie_id=m[4].id, hall_id=h[1].id, datetime=datetime(2026,5,5,21,0), price=380),
            ])
            db.session.commit()

    app.run(host="0.0.0.0", port=5000, debug=True)