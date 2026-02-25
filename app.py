from flask import Flask, render_template, request, jsonify
import sqlite3
import os

import requests  # Не забудь добавить в начало файла

app = Flask(__name__)


# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')


def get_db_connection():
    """Устанавливает соединение с базой данных."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Создает таблицу, если она еще не существует."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            coming TEXT,
            alcohol TEXT,
            allergy_info TEXT,
            wish TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("База данных инициализирована: " + DB_PATH)


@app.route('/')
def index():
    """Главная страница с формой."""
    return render_template('index.html')


@app.route('/api/rsvp', methods=['POST'])
def rsvp():
    """Принимает данные формы через POST-запрос (JSON)."""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Нет данных"}), 400

        # Извлекаем данные из JSON
        name = data.get('name', 'Не указано')
        phone = data.get('phone', 'Не указано')
        coming = data.get('coming', 'Не указано')

        # Алкоголь приходит как список, превращаем в строку через запятую
        alcohol_list = data.get('alcohol', [])
        alcohol_str = ", ".join(alcohol_list) if isinstance(alcohol_list, list) else str(alcohol_list)

        # Проверяем аллергию
        has_allergy = data.get('has_allergy', False)
        allergy_info = data.get('allergy_info', '') if has_allergy else "Нет"

        # Пожелания
        wish = data.get('wish', '')

        # Сохраняем в базу данных
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO guests (name, phone, coming, alcohol, allergy_info, wish)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, phone, coming, alcohol_str, allergy_info, wish))
        conn.commit()
        conn.close()

        print(f"Успешно сохранено: {name}")
        return jsonify({"success": True, "message": "Данные успешно сохранены"}), 200

    except Exception as e:
        print(f"Ошибка на сервере: {e}")
        return jsonify({"success": False, "message": str(e)}), 500



if __name__ == '__main__':
    # Инициализируем БД перед запуском сервера
    init_db()
    # Запуск сервера на порту 5000
    app.run(debug=True, port=5000)