from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Hello')
def hello():
    return 'Hello'

@app.route('/Hello/<name>')
def greeting(name):
    return f'Hello, {name}'


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', 404)

if __name__ == '__main__':
    app.run(debug = True)