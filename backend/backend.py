from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Дозволити CORS для всіх доменів

# Функція для підключення до бази даних
def connect_to_db():
    return mysql.connector.connect(
        user='admin',
        password='123qwe123',
        host='db',
        database='ads'
    )


# Створення таблиці
@app.route('/create_table', methods=['POST'])
def create_table():
    conn = None
    cursor = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ad (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip_address VARCHAR(45) NOT NULL,
                ad_text TEXT NOT NULL
            )
        """)
        return jsonify({"message": "Таблицю 'ad' успішно створено!"}), 201
    except Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Додавання оголошення
@app.route('/ads', methods=['POST'])
def add_ad():
    data = request.json
    ip_address = data.get('ip_address')
    ad_text = data.get('ad_text')
    
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ad (ip_address, ad_text) VALUES (%s, %s)", (ip_address, ad_text))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Запис успішно додано!"}), 201

# Отримання всіх оголошень
@app.route('/ads', methods=['GET'])
def get_all_ads():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ad")
    ads = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Форматування даних для відповіді
    ads_list = [{"id": ad[0], "ip_address": ad[1], "ad_text": ad[2]} for ad in ads]
    
    return jsonify(ads_list), 200

# Видалення всіх оголошень
@app.route('/ads', methods=['DELETE'])
def delete_all_ads():
    conn = None
    cursor = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ad")
        conn.commit()  # Підтвердження змін
        return jsonify({"message": "Усі записи успішно видалено!"}), 200
    except Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"}), 200

# Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Змінюйте порт, якщо потрібно
