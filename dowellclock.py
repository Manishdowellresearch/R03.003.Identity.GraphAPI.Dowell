from flask import Flask, jsonify, request, make_response , redirect, url_for, render_template, send_from_directory
import jwt
import os
import datetime

app=Flask(__name__)


@app.route('/dowellclock',methods=['GET'])
def clock():
    first_date = datetime.datetime(1970, 1, 1)
    time_since = datetime.datetime.now() - first_date
    t = int(time_since.total_seconds())
    t2 = "1609459200"
    answer = int(t)-int(t2)
    return jsonify({"DowellClock is":answer})

app.run()