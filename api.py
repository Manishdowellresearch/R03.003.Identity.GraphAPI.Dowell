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
CORS(app)

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

@app.route('/add/<num1>/<num2>',methods=['GET'])
@token_required
def sum(num1,num2):
    ans= int(num1) + int(num2)
    return jsonify({"answer":ans})

@app.route('/subtract/<num1>/<num2>',methods=['GET'])
@token_required
def sub(num1,num2):
    ans= int(num1) - int(num2)
    return jsonify({"answer":ans})


@app.route('/multiply/<num1>/<num2>',methods=['GET'])
@token_required
def mul(num1,num2):
    ans= int(num1) * int(num2)
    return jsonify({"answer":ans})

@app.route('/divide/<num1>/<num2>',methods=['GET'])
@token_required
def div(num1,num2):
    ans= int(num1) / int(num2)
    return jsonify({"answer":ans})

@app.route('/dowellclock',methods=['GET'])
def clock():
    import datetime
    first_date = datetime.datetime(1970, 1, 1)
    time_since = datetime.datetime.now() - first_date
    t = int(time_since.total_seconds())
    t2 = "1609459200"
    answer = int(t)-int(t2)
    return jsonify({"DowellClock is":answer})

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




@app.route('/token')
def a():
    token = jwt.encode({'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')})


if __name__ == '__main__':
    app.run()