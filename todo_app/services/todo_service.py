import random
import string
from repositories.todo_repo import (
    get_todos_by_user,
    create_todo,
    find_todo,
    update_todo,
    update_todo_status,
    delete_todo
)
from exceptions.exceptions import BadRequestException, NotFoundException

def generate_uid():
    chars = string.ascii_uppercase + string.digits
    return "TODO-" + ''.join(random.choices(chars, k=6))

def format_todo(todo):
    return {
        'id': todo['id'],
        'u_id': todo['u_id'],
        'title': todo['title'],
        'description': todo['description'],
        'created_at': str(todo['created_at']),
        'updated_at': str(todo['updated_at']),
        'completed': True if todo['completed'] else False
    }

def get_todos_service(user_id, show):
    todos = get_todos_by_user(user_id, show)
    return {"total": len(todos), "todos": [format_todo(t) for t in todos]}, 200

def create_todo_service(user_id, title, description):
    if not title:
        raise BadRequestException("title is required")
    u_id = generate_uid()
    todo = create_todo(u_id, user_id, title, description)
    return {"message": "Todo created successfully", "todo": format_todo(todo)}, 201

def update_todo_service(u_id, user_id, title, description, completed):
    if not title:
        raise BadRequestException("title is required")
    if not find_todo(u_id, user_id):
        raise NotFoundException(f"Todo '{u_id}' not found")
    todo = update_todo(u_id, title, description, completed)
    return {"message": "Todo updated successfully", "todo": format_todo(todo)}, 200

def update_status_service(u_id, user_id, completed):
    if completed is None:
        raise BadRequestException("completed field is required")
    if not find_todo(u_id, user_id):
        raise NotFoundException(f"Todo '{u_id}' not found")
    todo = update_todo_status(u_id, completed)
    return {"message": "Status updated successfully", "todo": format_todo(todo)}, 200

def delete_todo_service(u_id, user_id):
    if not find_todo(u_id, user_id):
        raise NotFoundException(f"Todo '{u_id}' not found")
    delete_todo(u_id)
    return {"message": f"Todo '{u_id}' deleted successfully"}, 200
