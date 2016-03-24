# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_file
import json
import os
import datetime
from flask import Response
import localimage
import os.path
import adapter

DEBUG = True

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route('/image/<path:id>')
def get_image(id):
    return send_file('/' + id, mimetype='image/gif')

@app.route('/thumb/<path:id>')
def get_thumb(id):
    return send_file(id, mimetype='image/gif')

@app.route('/images')
def get_images():
	adapter.init()
	files = adapter.create_thumbnails()
	result = { }

	for key, value in files.iteritems():
		result['/image' + key] = '/thumb/' + value

	return json.dumps(result)

if __name__ == "__main__":
    app.run(debug=True)