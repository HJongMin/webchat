from flask import Flask, render_template
from flask.ext.socketio import SocketIO

import redis
import threading
import time



app = Flask(__name__)
socketio = SocketIO(app)

r = redis.client.StrictRedis()

sub = r.pubsub()
sub.subscribe("test")

def listen():
        global temp
        for m in sub.listen():
                print m['data']
                if m['data']:
                        socketio.emit('msg', m['data'])
        return

t = threading.Thread(target = listen)
t.daemon = True
t.start()

def set_guest():
	global cnt
	cnt += 1
        nick = "Guest_" + str(cnt)
	return nick

@socketio.on('connect')
def conn():
	print 'Connection'
	socketio.send('conn')

@socketio.on('message')
def noname_event(msg):
	socketio.send(msg)
	return

@socketio.on('msg')
def msg(msg):
	r.publish('test', msg)
	print msg
	return	

@app.route('/')
def index():
	return render_template('ws_test.html')

@app.route('/chat')
def chat():
	nick = set_guest()
	return render_template('chat.html', nick = nick)

cnt = 0

if __name__ =='__main__':
	app.debug=True
	socketio.run(app)

#	app.run(debug = True)
