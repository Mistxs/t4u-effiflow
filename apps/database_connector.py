from datetime import datetime
from pytz import timezone

from flask import Blueprint, render_template, jsonify, request
from config import db_params, eddy_headers

import requests

db_connector = Blueprint('db_connector', __name__, url_prefix='/db_connector')


ts = datetime.now()
timezone = timezone('Etc/GMT-3')
ts_msk = ts.astimezone(timezone)

@db_connector.route('/supermod')
def index():
    return render_template('/supermod/demo.html', ts=ts_msk, title="DB_Connector")

