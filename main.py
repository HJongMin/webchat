from flask import Flask, render_template
from flask.ext.socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


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
	socketio.emit('msg', msg)

@app.route('/')
def index():
	return render_template('ws_test.html')
#	return "Hello, world!"

@app.route('/chat')
def chat():
#	cnt = cnt + 1	
#	nick = "Guest_" + cnt
	nick = set_guest()
	return render_template('chat.html', nick = nick)

cnt = 0

if __name__ =='__main__':
	app.debug=True
	socketio.run(app)


#	app.run(debug = True)
