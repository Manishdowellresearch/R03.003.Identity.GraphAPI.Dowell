from flask import Flask, jsonify, request, make_response , redirect, url_for, render_template, send_from_directory
import jwt
import os
import datetime
from functools import wraps
from flask_cors import CORS
import matplotlib.pyplot as plt
import io
import base64
from random import sample
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import sys

UPLOAD_FOLDER =r'/home/websitee/add/upload'

ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png','JPG','JPEG','PNG','csv'}

app= Flask(__name__,template_folder='/home/websitee/add/static')
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['SECRET_KEY'] = 'thisisthesecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/plot')
def build_plot():
    img = io.BytesIO()
    df = pd.read_csv('/home/websitee/add/data.csv')
    df.plot(kind= 'scatter',x = 'Duration', y = 'Maxpulse')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)


@app.route('/upload')
def upload_file():
   return render_template('index.html')


@app.route("/uploader",methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    img = io.BytesIO()
    df = pd.read_csv('/home/websitee/add/data.csv')
    df.plot(kind= 'scatter',x = 'Duration', y = 'Maxpulse')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)



@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run()