from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)


# Создание базы данных, если она не существует
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            site TEXT,
            event_type TEXT,
            event_data TEXT,
            timestamp TEXT
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


@app.route(
    "/track"
)  # Когда пользователь откроет страницу по адресу /track, вызови функцию track()
def track():  # получает данные из url и отдает их письму, чтобы оно появилось
    user_id = request.args.get(
        "user_id", "неизвестен"
    )  # возвращает строку; request.args — это объект, содержащий GET-параметры, переданные в URL.
    # .get("user_id") извлекает значение параметра user_id из URL; http://example.com/track?user_id=123
    site = request.args.get("site", "не указан")
    return render_template(
        "track.html", user_id=user_id, site=site
    )  # render_template — функция, которая рендерит HTML-шаблон с переменными.
    # внутри html можно использовать так: <p>User ID: {{ user_id }}</p>


@app.route(
    "/event", methods=["POST"]
)  # POST означает, что данные отправляются в теле запроса, а не в URL
def event():  # принимает события, отправляет их методом POST в формате JSON, извлекает инфц(кто отправил, с какого сайта, данные)
    data = request.json  # способ получить JSON-данные, присланные в теле POST-запроса
    user_id = data.get("user_id")
    site = data.get("site")
    event_type = data.get("event_type")
    event_data = str(data.get("event_data"))
    timestamp = datetime.isoformat()

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO events (user_id, site, event_type, event_data, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """,
        (user_id, site, event_type, event_data, timestamp),
    )
    conn.commit()
    conn.close()

    return jsonify(
        {"status": "success"}
    )  # возвращает ответ, что все хорошо. можно добавить js обработчика


@app.route(
    "/site/<site_name>"
)  # часть URL после /site/ должна быть передана как параметр site_name в функцию serve_static_site.
def serve_static_site(site_name):
    return send_from_directory(
        "static_sites", f"{site_name}.html"
    )  # функция, которая ищет файл с именем "{site_name}.html" в папке static_sites и отправляет его в ответ на запрос


if (
    __name__ == "__main__"
):  # if __name__ == "__main__": — эта конструкция проверяет, запущен ли данный скрипт напрямую (не импортирован в другом файле).
    app.run(host="0.0.0.0", port=5000)
# Указывает, что сервер будет доступен на всех сетевых интерфейсах устройства. приложение будет доступно не только локально (на localhost), но и на любом IP-адресе устройства
