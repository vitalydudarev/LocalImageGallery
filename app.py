# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_file
import json
import adapter
import worker

app = Flask(__name__)
worker_proxy = worker.WorkerProxy()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_images")
def get_images():
    adapter.init()
    result = worker_proxy.get_result(lambda image: __get_image_link(image), lambda thumb: __get_thumb_link(thumb))
    return json.dumps(result)

@app.route('/image/<path:id>')
def get_image(id):
    return send_file('/' + id, mimetype='image/gif')

@app.route('/thumb/<path:id>')
def get_thumb(id):
    return send_file(id, mimetype='image/gif')

def __get_image_link(image_name):
    return '/image' + image_name

def __get_thumb_link(thumb_name):
    return '/thumb/' + thumb_name

if __name__ == "__main__":
    app.run(debug=True)