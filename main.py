import json
from datetime import datetime
from pytz import timezone
from flask import Flask, render_template, Response
from apps.fiosplitter import fiosplitter
from apps.search import tsearch
from apps.fsr import fsr
from apps.unlocker import unlocker
from pageindex import pageindex
from apps.superbar import superbar
from apps.loadvisits import loadvisits
from apps.superloyal import superloyal
from apps.findoverpayed import overpay
from flask_cors import CORS

from apps.loadclients import loadclients

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Регистрация приложений
app.register_blueprint(fiosplitter)
app.register_blueprint(tsearch)
app.register_blueprint(fsr)
app.register_blueprint(unlocker)
app.register_blueprint(superbar)
app.register_blueprint(loadvisits)
app.register_blueprint(loadclients)
app.register_blueprint(superloyal)
app.register_blueprint(overpay)


ts = datetime.now()
timezone = timezone('Etc/GMT-3')
ts_msk = ts.astimezone(timezone)



@app.route('/')
def index():
    title = 'Стартовая'
    return render_template('index.html', title=title, active_page='start', ts=ts_msk)


@app.route('/<route>/<page_name>', methods = ['GET'])
def page_engine(route,page_name):
    title = pageindex[f"{page_name}"]
    return render_template(f'/{route}/{page_name}.html', title=title, active_page=page_name, route=route, ts=ts)


if __name__ == '__main__':
    app.run(port=3022)