from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash, session
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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

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
        'completion': '100%',
        'homework': '100%',
        'comments': 'Изучил работу авторизации во Flask'
        },
        {
        'name': 'Работа с REST API',
        'completion': '100%',
        'homework': '100%',
        'comments': 'Позанкомился с API. Узнал отличия от REST API'
        },
        {
        'name': 'Итоговый проект',
        'completion': '100%',
        'homework': '50%',
        'comments': 'В работе'
        },
        {
        'name': 'Итоговая аттестация',
        'completion': '100%',
        'homework': '70%',
        'comments': 'Очень сложный тест...'
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

    entries = Notes.query.filter_by(user_id=session['user_id']).all()
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
        new_entry = Notes(title=title, subtitle=subtitle, text=content, user_id=session['user_id'])
        db.session.add(new_entry)
        db.session.commit()

    except Exception as e:
        print(f'Ошибка: {e}')

    return redirect(url_for('diary'))


@app.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему для доступа к этой странице.', 'warning')
        return redirect(url_for('login'))

    entry = Notes.query.filter_by(id=entry_id, user_id=session['user_id']).first_or_404(entry_id)

    if request.method == 'POST':
        try:
            entry.title = request.form.get('title')
            entry.subtitle = request.form.get('subtitle')
            entry.text = request.form.get('content')

            db.session.commit()
            flash('Запись успешно обновлена!', 'success')
            return redirect(url_for('diary'))

        except Exception as e:
            print(f'Ошибка при редактировании: {e}')
            flash('Произошла ошибка при обновлении записи', 'error')

    return render_template('edit_entry.html', entry=entry)


@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему.', 'warning')
        return redirect(url_for('login'))

    entry = Notes.query.filter_by(id=entry_id, user_id=session['user_id']).first_or_404(entry_id)

    try:
        db.session.delete(entry)
        db.session.commit()
        flash('Запись успешно удалена!', 'success')
    except Exception as e:
        print(f'Ошибка при удалении: {e}')
        flash('Произошла ошибка при удалении записи', 'error')

    return redirect(url_for('diary'))


if __name__ == '__main__':
    app.run(debug = True)