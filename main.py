from flask import Flask, render_template, request, jsonify
from apps.fiosplitter import fiosplitter
from apps.search import tsearch


app = Flask(__name__)

# Регистрация приложений
app.register_blueprint(fiosplitter)
app.register_blueprint(tsearch)

app.static_folder = 'static'

# Роуты для вебстраниц (не действий)
from datetime import datetime, timedelta
import pytz

ts = datetime.now()
timezone = pytz.timezone('Etc/GMT-3')
ts_msk = ts.astimezone(timezone)


@app.route('/')
def index():
    title = 'Стартовая'
    return render_template('index.html', title=title, active_page='start', ts=ts_msk)

@app.route('/vnedrenie/<route>/<page_name>')
def vnedrenie_page(page_name,route):
    title = f'{page_name}'
    return render_template(f'vnedrenie/{route}/{page_name}.html', title=title, active_page=page_name, route='vnedrenie', ts=ts)

@app.route('/<route>/<page_name>')
def page_engine(route,page_name):
    title = f'{page_name}'
    return render_template(f'/{route}/{page_name}.html', title=title, active_page=page_name, route=route, ts=ts)


if __name__ == '__main__':
    app.run(port=3110)