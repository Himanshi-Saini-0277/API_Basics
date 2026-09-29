from db.connection import get_db

def find_user_by_username(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    db.close()
    return row

def get_all_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id, username FROM users")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows

def create_user(user_id, username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (user_id, username, password) VALUES (%s, %s, %s)", (user_id, username, password))
    db.commit()
    cursor.close()
    db.close()

def delete_user(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        db.close()
        return False
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    db.commit()
    cursor.close()
    db.close()
    return True

def update_user_password(username, new_password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
    db.commit()
    cursor.close()
    db.close()
