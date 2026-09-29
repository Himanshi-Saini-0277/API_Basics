from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hima@0277",
        database="flaskdb"
    )

def init_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hima@0277"
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS flaskdb")
    cursor.execute("USE flaskdb")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """)
    db.commit()
    cursor.close()
    db.close()

init_db()

def get_data():
    return request.get_json() if request.is_json else request.form

def json_or_render(template, error=None, **kwargs):
    if request.is_json:
        return jsonify({"error": error} if error else kwargs)
    return render_template(template, error=error)

@app.route('/')
def first():
    return redirect(url_for('login_page'))


@app.route('/register', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'])
def register_page():
    method = request.method

    if method == 'HEAD':
        return render_template('register.html')

    if method == 'GET':
        if request.is_json or request.args.get('format') == 'json':
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT id, username FROM users")
            rows = cursor.fetchall()
            cursor.close()
            db.close()
            user_list = [{'sr': i+1, 'username': row[1]} for i, row in enumerate(rows)]
            return jsonify({"total": len(user_list), "users": user_list}), 200
        return render_template('register.html')

    if method == 'OPTIONS':
        res = jsonify({"allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]})
        res.headers['Allow'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD'
        return res, 200

    if method == 'DELETE':
        data = get_data()
        username = data.get('username')
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            db.close()
            return jsonify({"error": "User not found"}), 404
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": f"User '{username}' deleted"}), 200

    data = get_data()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return json_or_render('register.html', error="Username and password are required"), 400

    if method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            return json_or_render('register.html', error="Username already exists"), 409
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        cursor.close()
        db.close()
        if request.is_json:
            return jsonify({"message": f"User '{username}' registered successfully"}), 201
        return redirect(url_for('login_page'))

    if method in ('PUT', 'PATCH'):
        old_password = data.get('old_password')
        if not old_password:
            return jsonify({"error": "old_password is required"}), 400
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            db.close()
            return jsonify({"error": "User not found"}), 404
        if row[0] != old_password:
            cursor.close()
            db.close()
            return jsonify({"error": "Old password is incorrect"}), 401
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (password, username))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({
            "message": f"Password updated for '{username}'",
            "username": username,
            "previous_password": old_password,
            "current_password": password
        }), 200


@app.route('/login', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'])
def login_page():
    method = request.method

    if method == 'HEAD':
        return render_template('login.html')

    if method == 'GET':
        if request.is_json or request.args.get('format') == 'json':
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT id, username FROM users")
            rows = cursor.fetchall()
            cursor.close()
            db.close()
            user_list = [{'sr': i+1, 'username': row[1]} for i, row in enumerate(rows)]
            return jsonify({"total": len(user_list), "users": user_list}), 200
        return render_template('login.html')

    if method == 'OPTIONS':
        res = jsonify({"allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]})
        res.headers['Allow'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD'
        return res, 200

    if method == 'DELETE':
        return jsonify({"message": "Session logged out successfully"}), 200

    data = get_data()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return json_or_render('login.html', error="Username and password are required"), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    db.close()

    if row and row[0] == password:
        if request.is_json:
            return jsonify({"message": f"Welcome, {username}!"}), 200
        return render_template('first.html', username=username)

    return json_or_render('login.html', error="Invalid username or password"), 401

@app.route('/logout')
def logout():
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
