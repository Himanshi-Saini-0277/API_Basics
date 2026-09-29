from db.connection import get_db

def get_todos_by_user(user_id, show):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if show == 'all':
        cursor.execute("SELECT * FROM todos WHERE user_id = %s", (user_id,))
    elif show == 'completed':
        cursor.execute("SELECT * FROM todos WHERE user_id = %s AND completed = TRUE", (user_id,))
    else:
        cursor.execute("SELECT * FROM todos WHERE user_id = %s AND completed = FALSE", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows

def create_todo(u_id, user_id, title, description):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO todos (u_id, user_id, title, description) VALUES (%s, %s, %s, %s)",
        (u_id, user_id, title, description)
    )
    db.commit()
    cursor.execute("SELECT * FROM todos WHERE u_id = %s", (u_id,))
    todo = cursor.fetchone()
    cursor.close()
    db.close()
    return todo

def find_todo(u_id, user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos WHERE u_id = %s AND user_id = %s", (u_id, user_id))
    row = cursor.fetchone()
    cursor.close()
    db.close()
    return row

def update_todo(u_id, title, description, completed):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        UPDATE todos SET title = %s, description = %s, completed = %s WHERE u_id = %s
    """, (title, description, completed, u_id))
    db.commit()
    cursor.execute("SELECT * FROM todos WHERE u_id = %s", (u_id,))
    todo = cursor.fetchone()
    cursor.close()
    db.close()
    return todo

def update_todo_status(u_id, completed):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("UPDATE todos SET completed = %s WHERE u_id = %s", (completed, u_id))
    db.commit()
    cursor.execute("SELECT * FROM todos WHERE u_id = %s", (u_id,))
    todo = cursor.fetchone()
    cursor.close()
    db.close()
    return todo

def delete_todo(u_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM todos WHERE u_id = %s", (u_id,))
    db.commit()
    cursor.close()
    db.close()
