const API_BASE = "http://127.0.0.1:5000";

async function loadAll() {
    await loadSchedule();
    await loadMovies();
    await loadPopular();
}

async function loadSchedule() {
    const container = document.getElementById("schedule-container");
    try {
        const res = await fetch(`${API_BASE}/api/schedule`);
        const data = await res.json();
        if (!data.length) {
            container.innerHTML = "<p style='color:#888;'>На сегодня сеансов нет</p>";
            return;
        }
        container.innerHTML = data.map(s => `
            <div class="schedule-card">
                <h3>${s.movie}</h3>
                <div class="meta">
                    <span>🕒 ${s.time}</span>
                    <span>🏢 ${s.hall}</span>
                    <span>🎭 ${s.genre}</span>
                    <span>⭐ ${s.rating}</span>
                </div>
                <div class="price">${s.price} ₽</div>
            </div>
        `).join("");
    } catch (e) {
        container.innerHTML = "<p style='color:#888;'>Не удалось загрузить расписание</p>";
    }
}

async function loadMovies(genre = "") {
    const container = document.getElementById("movies-container");
    const url = genre ? `${API_BASE}/api/search?genre=${genre}` : `${API_BASE}/api/movies`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        container.innerHTML = data.map(m => `
            <div class="movie-card">
                <div class="poster-placeholder">🎬</div>
                <div class="info">
                    <h3>${m.title}</h3>
                    <p>${m.genre}</p>
                    <span class="rating">⭐ ${m.rating}</span>
                </div>
            </div>
        `).join("");
    } catch (e) {
        container.innerHTML = "<p style='color:#888;'>Не удалось загрузить фильмы</p>";
    }
}

async function loadPopular() {
    const container = document.getElementById("popular-container");
    try {
        const res = await fetch(`${API_BASE}/api/popular`);
        const data = await res.json();
        container.innerHTML = data.map(m => `
            <div class="movie-card">
                <div class="poster-placeholder">🏆</div>
                <div class="info">
                    <h3>${m.title}</h3>
                    <p>${m.genre}</p>
                    <span class="rating">⭐ ${m.rating}</span>
                </div>
            </div>
        `).join("");
    } catch (e) {
        container.innerHTML = "<p style='color:#888;'>Не удалось загрузить топ</p>";
    }
}

async function searchByGenre() {
    const genre = document.getElementById("genre-input").value.trim();
    await loadMovies(genre);
}

loadAll();