import random
import string
from repositories.user_repo import (
    find_user_by_username,
    get_all_users,
    create_user,
    delete_user,
    update_user_password
)
from exceptions.exceptions import BadRequestException, ConflictException, NotFoundException, UnauthorizedException

def generate_user_id():
    chars = string.ascii_uppercase + string.digits
    return "USR-" + ''.join(random.choices(chars, k=6))

def register_user(username, password):
    if not username or not password:
        raise BadRequestException("username and password are required")

    if find_user_by_username(username):
        raise ConflictException("Username already exists")

    user_id = generate_user_id()
    create_user(user_id, username, password)
    return {"message": f"User '{username}' registered successfully", "user_id": user_id}, 201

def login_user(username, password):
    if not username or not password:
        raise BadRequestException("Username and password are required")

    row = find_user_by_username(username)
    if not row or row[1] != password:
        raise UnauthorizedException("Invalid username or password")

    return {"user_id": row[0], "username": username}, 200

def delete_user_service(username):
    if not username:
        raise BadRequestException("username is required")

    if not delete_user(username):
        raise NotFoundException(f"User '{username}' not found")

    return {"message": f"User '{username}' deleted"}, 200

def update_password_service(username, old_password, new_password):
    if not username or not old_password or not new_password:
        raise BadRequestException("username, old_password and password are required")

    row = find_user_by_username(username)
    if not row:
        raise NotFoundException(f"User '{username}' not found")

    if row[1] != old_password:
        raise UnauthorizedException("Old password is incorrect")

    update_user_password(username, new_password)
    return {"message": f"Password updated for '{username}'", "previous_password": old_password, "current_password": new_password}, 200

def list_users_service():
    rows = get_all_users()
    return {"total": len(rows), "users": [{"sr": i+1, "user_id": r[0], "username": r[1]} for i, r in enumerate(rows)]}, 200
