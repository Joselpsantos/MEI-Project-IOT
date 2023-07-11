from flask import Flask, render_template
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import netifaces


app = Flask(__name__)
socketio = SocketIO (app) 


temp_topic = 'temperature'
control_topic = 'control'
server = 'localhost'
MQTTport = 1883
client = None
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

# SocketIO

@socketio.on('connect')
def on_connect():
    print('Socket client connected.')
    socketio.emit('receive', "Ligao ao broker")

@socketio.on('ledControl')
def on_publish(payload):
    client.publish(control_topic, payload)
    print(payload)

# MQTT

def on_connect(client, userdata, flags, rc):

    socketio.emit('receive', "Status: connected to broker")
    client.subscribe(temp_topic, qos=0)
    client.subscribe(control_topic, qos=0)

def on_message(client, userdata, msg):
    socketio.send(msg.payload.decode())
    print("On message " + msg.payload.decode())

# HTTP

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config')
def config():
    render_template("config_mqtt.html")

# Main

def getIp():
    addresses = netifaces.ifaddresses("enp0s8")
    ip_address = addresses[netifaces.AF_INET][0]['addr']
    return ip_address

client = mqtt.Client("Mqtt-socket-bridge-2021", clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("pico", "pico")
client.connect(server, MQTTport, keepalive=60)

print('Starting the MQ loop..')
client.loop_start()

print('Starting the socket server on port 5000...')
socketio.run(app, host=getIp(), port=5001, debug=True)
