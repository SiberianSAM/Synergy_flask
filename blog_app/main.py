from flask import Flask, render_template

app = Flask(__name__)

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
        'homework': '99%',
        'comments': 'Лучше разобрался в HTML и CSS'
        },
        {
        'name': 'Шаблоны и формы Flask',
        'completion': '0%',
        'homework': '0%',
        'comments': 'Ожидает выполнения'
        },
        {
        'name': 'Основы Flask SQLAlchemy',
        'completion': '0%',
        'homework': '0%',
        'comments': 'Ожидает выполнения'
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

@app.route('/Hello')
def hello():
    return 'Hello'

if __name__ == '__main__':
    app.run(debug = True)