from flask import Flask, render_template, request, jsonify


# from resafe import *
import re

app = Flask(__name__)

# Регистрация приложений
# app.register_blueprint(fsr)

app.static_folder = 'static'

# Роуты для вебстраниц (не действий)

@app.route('/')
def index():
    title = 'Стартовая'
    return render_template('index.html', title=title, active_page='start')

@app.route('/vnedrenie/<route>/<page_name>')
def vnedrenie_page(page_name,route):
    title = f'{page_name}'
    return render_template(f'vnedrenie/{route}/{page_name}.html', title=title, active_page=page_name, route='vnedrenie')

@app.route('/<route>/<page_name>')
def page_engine(route,page_name):
    title = f'{page_name}'
    return render_template(f'/{route}/{page_name}.html', title=title, active_page=page_name, route='vnedrenie')


if __name__ == '__main__':
    app.run(port=4010)