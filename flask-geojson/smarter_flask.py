# -*- coding: utf-8 -*-
import platform, sys
import os
import io
import base64
import json
#home_dir=[r".\DLLs", r"sitelib.zip", r'site-packages.zip']
#sys.path = [os.path.join(os.getcwd(), a) for a in home_dir]
#print ('\n'.join(sys.path))
#from __future__ import unicode_literals  # Use u"unicode strings"
from os import urandom, chdir, listdir, path
import datetime as dt
today = dt.datetime.now().date()

from flask import Response, Flask, flash, render_template, render_template_string, send_from_directory, make_response
from flask_restful import Resource, Api, reqparse

app = Flask(__name__, template_folder='.')
app.jinja_env.autoescape = True
app.secret_key = urandom(24)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

api = Api(app)
hostname='127.0.0.1'
port=8000

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

@app.route('/plots')
def plots():
    Regionlist = ['Brazil',
    'Argentina',
    'France',
    'Spain',
    'Peru']
    return render_template('static/covid_dask.html', regions=Regionlist)

@app.route('/api/fetch')
def fetch():
    binaryData = b"00101010"
    runNumber = "100"
    Regionlist = ['Chile', 'Brazil', 'Uruguay', 'Bolivia', 'Paraguay']
    some_object = {
        "regions": Regionlist,
        "title": "my title"
        #"title": str(base64.b64encode(binaryData).decode()),
        #"hashdata": base64.b64encode(binaryData).decode(),
        }

    response = make_response(json.dumps(some_object, ensure_ascii=False))
    #response.headers["Content-Disposition"] = "attachment; filename=" + runNumber + ".geojson"
    #response.headers['X-Extra-Info-JSON'] = json.dumps(some_object)
    return response

@app.route("/static/<path:path>")
def getserve(path):
    for path in (
        safe_join(app.root_path, "static", path)
    ):
        if os.path.isfile(path):
            return send_file(path)
    abort(404)

@app.route('/')
def home():
    Regionlist = ['Chile', 'Brazil', 'Uruguay', 'Bolivia', 'Paraguay']
    return render_template('static/appjson.html')

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

request=[]
class RegionHandler(Resource):
    def __init__(self):
        self.n = 0
    def get(self, todo_id):
        if todo_id not in request:
            request.append(todo_id)
            R = None
            print(request)
            return Response(R, mimetype='image/png')
        else:
            sleep(1)
        self.n+=1

    def delete(self, todo_id):
        #del GIT[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        redirect("/");
        return task, 201

api.add_resource(RegionHandler, '/api/regions/<string:todo_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
