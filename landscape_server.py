from flask import render_template
from flask import Flask

from networkx.readwrite import json_graph
import networkx as nx
import community
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import requests
import mediacloud
import json
import os
import copy
import cPickle

from mediacloudlandscape.landscape import *

# Berkman Projects Directory
berkman_projects = os.environ['BKP']
api_key = cPickle.load( file( os.path.expanduser( berkman_projects + '/MediaCloud/mediacloud_api_key.pickle' ), 'r' ) )
mc = mediacloud.api.MediaCloud(api_key)
print(api_key)

def get_dumps(controversy_id):
    query = 'https://api.mediacloud.org/api/v2/controversy_dumps/list?controversies_id=%s&key=%s' % (controversy_id, api_key)
    return json.loads(requests.get(query).text)

def list_dumps(controversy_id):
    print('Dumps for Controversy ID %s:' % (controversy_id))
    dumps = get_dumps(controversy_id)
    for d in dumps:
        print('-%s [%s through %s]' % (d['controversy_dumps_id'], d['start_date'], d['end_date']))
    print('\n')
    return dumps

# For Community Detection / color coding programmatically:
#   http://nbviewer.ipython.org/github/dcalacci/hubway-vis/blob/master/notebooks/Visualizing%20hubway%20data%20using%20sigma.js.ipynb

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Media Cloud Landscapes</h1>'

# Test: 977, 865, 7197

# @app.route('/landscape/<int:controversy_id>/<int:dump_id>/<int:timeslice_id>')
@app.route('/landscape')
def landscape():
	# create_landscape(controversy_id, dump_id, timeslice_id)
	return render_template('sigma_test.html')

@app.route('/landscape_live/<int:controversy_id>/<int:dump_id>/<int:timeslice_id>')
def landscape_live(controversy_id, dump_id, timeslice_id):
	gexf_path = create_landscape(controversy_id, dump_id, timeslice_id)
	return render_template('sigma_test.html', gexf_path=gexf_path)

@app.route('/dumps/<int:dump_id>')
def dumps(dump_id):
	ds = list_dumps(dump_id)
	return render_template('dumps.html', dump_id=dump_id, dumps=ds)
	# return str([d['controversy_dumps_id'] for d in ds])

if __name__ == '__main__':
    app.run(debug=True)

