from flask import Flask, redirect, url_for
from config.settings import SECRET_KEY
from config.init_db import init_db
from routes.auth import auth
from routes.todos import todos

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth)
app.register_blueprint(todos)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
