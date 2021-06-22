#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify

from modulos.moneda import moneda

from waitress import serve

from apscheduler.schedulers.background import BackgroundScheduler 

v = moneda()

app = Flask(__name__)


def test_job():
	for i,x in enumerate([['BRL', 'COP'], ['BRL','CLP'], ['COP','BRL'], ['COP','CLP'], ['CLP','BRL'], ['CLP','COP']]):
		v.getURL(x, i) 
		print('#####################################################')

scheduler = BackgroundScheduler() 
job = scheduler.add_job(test_job, 'interval', minutes=10) 
scheduler.start()

@app.route('/', methods=['GET'])
def index():
	return ':)'

@app.route('/convert/<string:query>', methods=['GET'])
def get_data(query):
	# return query
	queries = query.split(',')

	queries = v.get_data(queries)

	return jsonify(queries)



@app.route('/run_bot', methods=['GET'])
def run_bot():

	for i,x in enumerate([['BRL', 'COP'], ['BRL','CLP'], ['COP','BRL'], ['COP','CLP'], ['CLP','BRL'], ['CLP','COP']]):
		v.getURL(x, i)

	return 'db actualizada'
@app.route('/get_all_data', methods=['GET'])
def get_all_data():

	return jsonify(v.get_all_data())

if __name__ == '__main__':
	serve(app, host='0.0.0.0', port=5000)