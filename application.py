import os

from flask import Flask, request, render_template, redirect, url_for,flash, session
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = os.urandom(12)
socketio = SocketIO(app)

nicknames=[]
list_channels=[]

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

class Channel:
    counter = 1
    def __init__(self, name):
        self.id = Channel.counter
        Channel.counter += 1
        self.name = name
        self.last_messages=[]

class Message:
    def __init__(self, nickname, timestamp, message):
        self.nickname = nickname
        self.timestamp = timestamp
        self.message = message

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
            session['nickname']=new_user.nickname
            return redirect(url_for('channels'))
    return render_template("enter.html")

@app.route("/channels", methods=["GET","POST"])
def channels():
    try:
        session['nickname']
        return render_template("channels.html")
    except KeyError:
        error='Pick a nickname to start chatting!'
        flash(error)
        return redirect(url_for('enter'))

@app.route("/channel", methods=["POST"])
def channel():
    error = None
    if request.method == 'POST':
        channel_name = request.form.get("new_channel")
        if any(c.name == channel_name for c in list_channels):
            error = 'Channel name already exists. Please pick another one.'
            flash(error)
            return render_template(url_for('channels'))
        else:
            new_channel = Channel(channel_name)
            list_channels.append(new_channel)
            return redirect(url_for('get_channel', channel_id=new_channel.id))

@app.route("/channel/<channel_id>")
def get_channel(channel_id):
    chan = filter(lambda c: c.id == channel_id,list_channels)
    return render_template("channel.html",channel=channel)
