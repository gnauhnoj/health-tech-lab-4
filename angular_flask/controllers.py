import os
import json

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort
from data_processing.analysis import get_data_over_period, handle_analysis_request, handle_recc_request
from angular_flask import app, data

# routing for API endpoints, generated from the models designated as API_MODELS
from angular_flask.models import *


# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/graphs')
@app.route('/analysis')
@app.route('/recommendations')
def basic_pages(**kwargs):
    return make_response(open('angular_flask/templates/index.html').read())


# routing for CRUD-style endpoints
# passes routing onto the angular frontend if the requested resource exists
crud_url_models = app.config['CRUD_URL_MODELS']


@app.route('/api/analysisdata', methods=['POST'])
def analysis_data():
    req = json.loads(request.data)
    date_intervals = [[datestr.split('T')[0] for datestr in dates] for dates in req['dates']]
    out = handle_analysis_request(data, date_intervals)
    return json.dumps(out)


@app.route('/api/graphdata', methods=['GET'])
def graph_data():
    out = {}
    out['x'], out['y_steps'], out['y_sed_act'], out['y_med_act'] = get_data_over_period(data, serialize_dates=True)
    return json.dumps(out)


@app.route('/api/reccdata', methods=['GET'])
def recc_data():
    out = handle_recc_request(data)
    return json.dumps(out)


# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
