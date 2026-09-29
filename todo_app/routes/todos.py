from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from services.todo_service import (
    get_todos_service,
    create_todo_service,
    update_todo_service,
    update_status_service,
    delete_todo_service
)

todos = Blueprint('todos', __name__)

def get_data():
    return request.get_json(force=True, silent=True) or request.form

def is_logged_in():
    return 'user_id' in session

@todos.route('/todos', methods=['GET'])
def get_todos():
    if not is_logged_in():
        if request.is_json:
            return jsonify({"error": "Please login first"}), 401
        return redirect(url_for('auth.login'))

    response, status = get_todos_service(session['user_id'], request.args.get('show'))

    if request.is_json:
        return jsonify(response), status
    return render_template('todos.html', todos=response['todos'], username=session['username'], enumerate=enumerate)

@todos.route('/todos', methods=['POST'])
def create_todo():
    if not is_logged_in():
        return jsonify({"error": "Please login first"}), 401

    data = get_data()
    response, status = create_todo_service(session['user_id'], data.get('title'), data.get('description', ''))
    return jsonify(response), status

@todos.route('/todos/<string:u_id>', methods=['PUT'])
def update_todo(u_id):
    if not is_logged_in():
        return jsonify({"error": "Please login first"}), 401

    data = get_data()
    response, status = update_todo_service(u_id, session['user_id'], data.get('title'), data.get('description', ''), data.get('completed', False))
    return jsonify(response), status

@todos.route('/todos/<string:u_id>', methods=['PATCH'])
def update_status(u_id):
    if not is_logged_in():
        return jsonify({"error": "Please login first"}), 401

    data = get_data()
    response, status = update_status_service(u_id, session['user_id'], data.get('completed'))
    return jsonify(response), status

@todos.route('/todos/<string:u_id>', methods=['DELETE'])
def delete_todo(u_id):
    if not is_logged_in():
        return jsonify({"error": "Please login first"}), 401

    response, status = delete_todo_service(u_id, session['user_id'])
    return jsonify(response), status
