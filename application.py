import os

from flask import Flask, request, render_template, redirect, url_for,flash
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = os.urandom(12)
socketio = SocketIO(app)

nicknames=[]

@app.route("/")
def index():
    return "Project 2: TODO"

class User:
    def __init__(self,nickname):
        self.nickname = nickname
        self.last_channel=None
    
    def set_last_channel(self,last_channel):
        self.last_channel = last_channel
        session['last_channel']=last_channel

@app.route("/enter", methods=["POST","GET"])
def enter():
    error=None
    if request.method == 'POST':
        nickname = request.form.get("nickname")
        if nickname in nicknames:
            error = 'Nickname already exists. Please choose another one.'
            flash(error)
            return render_template("enter.html")
        else:
            new_user = User(nickname)
            nicknames.append(nickname)
            session["nickname"]=new_user.nickname
            return redirect(url_for('channels'))
    return render_template("enter.html")

@app.route("/channels", methods=["GET","POST"])
def channels():
    return render_template("channels.html")