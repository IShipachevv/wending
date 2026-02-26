from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# Замените User на вашу модель
from flask_sqlalchemy import SQLAlchemy
import requests  # Не забудь добавить в начало файла

app = Flask(__name__)

# Настраиваем путь к базе данных
# Если мы на Render, возьмем ссылку из DATABASE_URL. Если дома — создаем файл wedding.db
uri = os.environ.get('DATABASE_URL', 'sqlite:///wedding.db')

# Фикс для Render: они дают ссылки postgres://, а SQLAlchemy просит postgresql://
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем базу данных
db = SQLAlchemy(app)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50))  # Например: 'приду', 'не приду'

    def __repr__(self):
        return f'<Guest {self.name}>'


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
    with app.app_context():
        db.create_all()  # Создаст таблицы, если их еще нет
    app.run(debug=True)