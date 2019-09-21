import os

from flask import Flask, request, render_template, redirect, url_for,flash, session
from flask_socketio import SocketIO, emit
import requests
import collections
from datetime import datetime
import json
import random

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = os.urandom(12)
socketio = SocketIO(app)

nicknames=[]
users=[]
#list_channels=[]

@app.route("/")
def index():
    #return "Project 2: TODO"
    return render_template("layout.html")


class User:
    def __init__(self,nickname):
        self.nickname = nickname
        self.last_channel=None
        self.color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
    def set_last_channel(self,last_channel):
        self.last_channel = last_channel
        session['last_channel']=last_channel

class Channel:
    counter = 1
    def __init__(self, name, password=None):
        self.id = Channel.counter
        Channel.counter += 1
        self.name = name
        self.password = password
        self.last_messages=collections.deque(maxlen=100)

    def add_message(self, message):
        if len(self.last_messages) < 100:
            self.last_messages.append(message)
        else:
            self.last_messages.popleft()
            self.last_messages.append(message)

list_channels=[Channel('Hola'),Channel('Chau'),Channel('Nombre re largo'),Channel('H'),Channel('12345678912345678912346'),Channel('asdfghjklzxcvbn')]

class Message:
    def __init__(self, nickname, timestamp, message, color):
        self.nickname = nickname
        self.timestamp = timestamp
        self.message = message
        self.color = color

    def to_json(self):
        return({"nickname": self.nickname, "timestamp": self.timestamp, "message": self.message, "color": self.color})

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
            users.append(new_user)
            print(get_user_by_nickname(new_user.nickname).color)
            session['nickname']=new_user.nickname
            return redirect(url_for('channels'))
    return render_template("enter.html")

@app.route("/channels", methods=["GET","POST"])
def channels():
    try:
        session['nickname']
        return render_template("channels.html", channels=filter(lambda channel : channel.password is None,list_channels))
    except KeyError:
        error='Pick a nickname to start chatting!'
        flash(error)
        return redirect(url_for('enter'))

@app.route("/channel", methods=["POST"])
def channel():
    error = None
    if request.method == 'POST':
        channel_name = request.form.get("new-channel")
        password = request.form.get("psw")
        if any(c.name == channel_name for c in list_channels):
            error = 'Channel name already exists. Please pick another one.'
            flash(error)
            return render_template("channels.html", channels = list_channels)
        else:
            new_channel = Channel(channel_name, password)
            list_channels.append(new_channel)
            return redirect(url_for('get_channel', channel_id=new_channel.id))

@app.route("/channel/<channel_id>")
def get_channel(channel_id):
    active_channel=get_channel_by_id(channel_id)
    session['active_channel'] = active_channel.id
    user = get_user_by_nickname(session['nickname'])
    return render_template("channel.html",channel=active_channel, color=user.color)

@app.route("/secchannel", methods=["POST"])
def get_secret_channel():
    error=None
    if request.method == 'POST':
        channel_name = request.form.get("secret_channel")
        password = request.form.get("psw")
        matching_channels = list(filter(lambda channel: channel.name == channel_name and channel.password == password, list_channels))
    if len(matching_channels) != 0:
        secret_channel_id = matching_channels[0].id
        print(secret_channel_id)
        print(matching_channels[0].name)
    return redirect(url_for('get_channel', channel_id=secret_channel_id))

        

def get_channel_by_id(channel_id):
    return(list(filter(lambda c: c.id == int(channel_id),list_channels))[0])

def get_user_by_nickname(nickname):
    return(list(filter(lambda u: u.nickname == nickname, users))[0])

@socketio.on("submit message")
def message(data):
    print(data['message'])
    print(data['color'])
    channel = get_channel_by_id(session['active_channel'])
    message = Message(session['nickname'],datetime.now().strftime("%H:%M:%S"),data['message'], data['color'])
    message_json = json.dumps(message, default=lambda x: x.__dict__)
    msg = message.to_json()
    channel.add_message(msg)
    print(channel.last_messages)
    emit("announce", msg, broadcast=True, include_self=True)


if __name__ == '__main__':
    socketio.run(app)