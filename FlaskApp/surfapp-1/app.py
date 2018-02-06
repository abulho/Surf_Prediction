from flask import Flask, render_template, request, jsonify, make_response
import os
import sys
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
