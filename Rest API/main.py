import sqlite3
from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from prompt_toolkit.shortcuts import confirm
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
diary_entries = {}
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///synergy_flask.db"
app.secret_key = "salt_corrodes_the_eyes"


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(24), nullable = False)
    subtitle = db.Column(db.String(15), nullable = True)
    text = db.Column(db.String(68), nullable = False)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/index')
def index():
    if 'user_id' not in session:
        flash(f'Пожалуйста, войдите в систему для доступа к этой странице.', 'warning')
        return redirect(url_for('login'))

    disciplines = [
        {
        'name': 'Основы Flask',
        'completion': '100%',
        'homework': '100%',
        'comments': 'Освоил микрофрейворк Flask'
        },
        {
        'name': 'HTML & CSS',
        'completion': '100%',
        'homework': '100%',
        'comments': 'Лучше разобрался в HTML и CSS'
        },
        {
        'name': 'Шаблоны и формы Flask',
        'completion': '100%',
        'homework': '100%',
        'comments': 'Разобрался с наследованием и базовыми шаблонами'
        },
        {
        'name': 'Основы Flask SQLAlchemy',
        'completion': '100%',
        'homework': '100%',
        'comments': 'Изучил SQLAlchemy и миграции БД'
        },
        {
        'name': 'Авторизация Flask',
        'completion': '90%',
        'homework': '95%',
        'comments': 'Ожидает проверки'
        },
        {
        'name': 'Работа с REST API',
        'completion': '0%',
        'homework': '0%',
        'comments': 'Ожидает выполнения'
        },
        {
        'name': 'Итоговый проект',
        'completion': '0%',
        'homework': '0%',
        'comments': 'Ожидает выполнения'
        },
        {
        'name': 'Итоговая аттестация',
        'completion': '0%',
        'homework': '0%',
        'comments': 'Ожидает выполнения'
        }
    ]
    return render_template('index.html', disciplines = disciplines)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not  password:
            flash('Все поля обазательны для заполнения', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Пароли не совпадают!', 'error')
            return render_template('register.html')

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()
            flash('Регистрация прошла успешна! Ещё один счастлиый пользователь зарегистрирован!', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            print(f'Ошибка при создании пользователя: {e}')

    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash(f'Заполните все поля', 'error')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Добро пожаловать, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash(f'Вы успешно вышли из системы!', 'info')
    return redirect(url_for('login'))

@app.route('/diary')
def diary():
    if 'user_id' not in session:
        flash(f'Пожалуйста, войдите в систему для доступа к этой странице.', 'warning')
        return redirect(url_for('login'))

    entries = Notes.query.all()
    return render_template('diary.html', entries = entries)


@app.route('/add_entry', methods=['POST'])
def add_entry():
    if 'user_id' not in session:
        flash(f'Пожалуйста, войдите в систему для доступа к этой странице.', 'warning')
        return redirect(url_for('login'))

    title = request.form.get('title')
    content = request.form.get('content')
    subtitle = request.form.get('subtitle')

    try:
        new_entry = Notes(title=title, subtitle=subtitle, text=content)
        db.session.add(new_entry)
        db.session.commit()

    except Exception as e:
        print(f'Ошибка: {e}')

    return redirect(url_for('diary'))

# REST API

# Запросы - GET
# @app.route('/api/get', methods=['GET'])
# def get_info():
#     conn = sqlite3.connect('instance/synergy_flask.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM users')
#     data = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return jsonify(data)

@app.route('/api/get', methods=['GET'])
def get_info():
    data = Notes.query.all()
    data_list = []
    for d in data:
        data_list.append(
            {
                'id': d.id,
                'title': d.title,
                'subtitle': d.subtitle,
                'text': d.text
            })
    return jsonify(data_list)

# Запросы - POST
@app.route('/api/post', methods=['POST'])
def create_notes():
    notes = request.get_json()
    new_note = Notes(
        title =  notes['title'],
        subtitle = notes['subtitle'],
        text =  notes['text']
    )
    db.session.add(new_note)
    db.session.commit()

    return f'ЗАПИСЬ добавлена, 201'

 # Для проверки
 # curl -X POST http://127.0.0.1:5000/api/post \
 #  -H "Content-Type: application/json" \
 #  -d '{
 #    "title": "Test",
 #    "subtitle": "Something",
 #    "text": "Notes created methods POST"
 #  }'


# Запросы - PUT
@app.route('/api/put/<int:notes_id>', methods=['PUT'])
def put_notes(notes_id):
    notes = Notes.query.get(notes_id)
    data = request.get_json()

    if 'title' in data:
        if not data['tite']:
            return jsonify('ERROR, title can not be empty')
        notes.title = data['title']

    if 'subtitle' in data:
        if not data['subtitle']:
            return jsonify('ERROR, subtitle can not be empty')
        notes.subtitle = data['subtitle']

    if 'text' in data:
        if not data['text']:
            return jsonify('ERROR, text can not be empty')
        notes.text = data['text']

    db.session.commit()
    return f'Заметка с ID {notes_id} обновлена ,200'

 # Для проверки
# curl -X PUT http://127.0.0.1:5000/api/put/5 \
#   -H "Content-Type: application/json" \
#   -d '{
#     "text": "Only text modify", "subtitle": "Modify"
#   }'

 # Запросы - DELETE
@app.route('/api/del/<int:notes_id>', methods=['DELETE'])
def delete_note(notes_id):
    data = Notes.query.get(notes_id)
    db.session.delete(data)
    db.session.commit()
    return f'Запись с ID - {notes_id} удалена!'

# Для проверки
# curl -X DELETE http://127.0.0.1:5000/api/del/6


# REST API


if __name__ == '__main__':
    app.run(debug = True)