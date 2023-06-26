import eventlet
import json
import netifaces
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
#app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'pico'
app.config['MQTT_PASSWORD'] = 'pico'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

topic1 = "temperature"
topic2 = "control"

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       print(getIp())
       mqtt.subscribe(topic1)
       mqtt.subscribe(topic2) # subscribe topic
        # subscribe topic
   else:
       print('Bad connection. Code:', rc)
       
       
@app.route('/')
def index():
    print(socket.gethostbyname(socket.gethostname()))
    return render_template('index.html')
    
@socketio.on("ledControl")
def handle_connect(message):
    mqtt.publish(topic1, message)
    print(message)
    
@socketio.on('connect')
def handle_connect():
    
    print("Connected to the frontend")

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(topic1, data['message'])

@app.route('/config')
def config():
    render_template("config_mqtt.html")

#@socketio.on('subscribe')
#def handle_subscribe():
#    mqtt.subscribe(topic) 
#    print("Subscrito")


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('receive', data=data)
    print(message)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

def getIp():
    addresses = netifaces.ifaddresses("enp0s8")
    ip_address = addresses[netifaces.AF_INET][0]['addr']
    return ip_address
    
if __name__ == '__main__':
    socketio.run(app, host= getIp(), port=5001, use_reloader=False, debug=True)
    
