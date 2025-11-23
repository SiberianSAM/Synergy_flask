from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
diary_entries = {}

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
        'homework': '98%',
        'comments': 'Ожидает проверки'
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

@app.route('/diary')
def diary():
    return render_template('diary.html', entries=diary_entries)


@app.route('/add_entry', methods=['POST'])
def add_entry():
    title = request.form.get('title')
    content = request.form.get('content')

    if title and content:
        diary_entries[title] = {
            'content': content,
            'timestamp': 'Сегодня'
        }

    return redirect(url_for('diary'))


if __name__ == '__main__':
    app.run(debug = True)