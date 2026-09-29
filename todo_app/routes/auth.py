from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from services.auth_service import register_user, login_user, delete_user_service, update_password_service, list_users_service

auth = Blueprint('auth', __name__)

def get_data():
    return request.get_json(force=True, silent=True) or request.form

@auth.route('/register', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'])
def register():
    method = request.method

    if method == 'HEAD':
        return render_template('register.html')

    if method == 'GET':
        if request.is_json or request.args.get('format') == 'json':
            response, status = list_users_service()
            return jsonify(response), status
        return render_template('register.html')

    if method == 'OPTIONS':
        res = jsonify({"allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]})
        res.headers['Allow'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD'
        return res, 200

    if method == 'DELETE':
        data = get_data()
        response, status = delete_user_service(data.get('username'))
        return jsonify(response), status

    data = get_data()

    if method == 'POST':
        response, status = register_user(data.get('username'), data.get('password'))
        if request.is_json:
            return jsonify(response), status
        return redirect(url_for('auth.login'))

    if method in ('PUT', 'PATCH'):
        response, status = update_password_service(data.get('username'), data.get('old_password'), data.get('password'))
        return jsonify(response), status

@auth.route('/login', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'])
def login():
    method = request.method

    if method == 'HEAD':
        return render_template('login.html')

    if method == 'GET':
        if request.is_json or request.args.get('format') == 'json':
            response, status = list_users_service()
            return jsonify(response), status
        return render_template('login.html')

    if method == 'OPTIONS':
        res = jsonify({"allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]})
        res.headers['Allow'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD'
        return res, 200

    if method == 'DELETE':
        session.clear()
        return jsonify({"message": "Session logged out successfully"}), 200

    data = get_data()
    user, status = login_user(data.get('username'), data.get('password'))

    session['username'] = user['username']
    session['user_id'] = user['user_id']

    if request.is_json:
        return jsonify({"message": f"Welcome, {user['username']}!", "user_id": user['user_id']}), 200
    return redirect(url_for('todos.get_todos'))

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
