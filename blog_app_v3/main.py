from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)
diary_entries = {}
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///synergy_flask.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(24), nullable = False)
    subtitle = db.Column(db.String(15), nullable = True)
    text = db.Column(db.String(68), nullable = False)



@app.route('/')
def index():
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
        'homework': '97%',
        'comments': 'Ожидает проверки'
        },
        {
        'name': 'Авторизация Flask',
        'completion': '0%',
        'homework': '0%',
        'comments': 'Ожидает выполнения'
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

@app.route('/diary')
def diary():
    entries = Notes.query.all()
    return render_template('diary.html', entries = entries)


@app.route('/add_entry', methods=['POST'])
def add_entry():
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

if __name__ == '__main__':
    app.run(debug = True)