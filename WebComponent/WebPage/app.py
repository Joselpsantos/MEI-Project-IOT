import logging

import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from datetime import datetime
import netifaces
#from flask_ngrok import run_with_ngrok
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'flask_mqtt'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_USERNAME'] = 'pico'
app.config['MQTT_PASSWORD'] = 'pico'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
app.config['MQTT_LAST_WILL_QOS'] = 2

MESSAGE_LOG_FILE = 'message_log.txt'

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

log_file = open(MESSAGE_LOG_FILE, 'a')

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
#run_with_ngrok(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ip')
def getIpEnd():
    return getIp()

@socketio.on('led')
def handle_publish(json_str):
    #connection_id = request.sid  # Get the connection ID
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f'[{timestamp}]  Message: {json_str}\n'
    mqtt.publish("control", json_str, 0)
    print(json_str)
    log_file.write(message)  # Write the message to the log file
    log_file.flush()  # Flush the file to ensure immediate write

@socketio.on('auto')
def handle_publish(json_str):
    mqtt.publish("control", "\"AUTO\"," + json_str, 0)
    print("auto " + json_str)  

@socketio.on('subscribe')
def handle_subscribe(json_str):
    #data = json.loads(json_str)
    mqtt.subscribe("control", 0)
    print("Subscribed: control")
    mqtt.subscribe("temperature")
    print("Subscribed: temperature")
    
@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()

@socketio.on('page_close')
def handle_page_close(msg):
    print("Page closed")
    mqtt.publish("control", "unsubscribe", 0)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payload = message.payload.decode()  # Convert payload to string
    topic = message.topic
    qos = message.qos
    retained = message.retain
    data = {
        'payload': payload,
        'topic': topic,
        'qos': qos,
        'retained': retained
    }
    message = f'[{timestamp}] Topic: {topic}, Payload: {payload}\n'
    if data['topic'] == "control" :
        print("Message received on topic: " + data["topic"] + " with the message: " + data["payload"])
        if data["payload"] != "on" or data["payload"] != "off" or data["payload"] != "unsubscribe":
            socketio.emit('led_status', data=data["payload"])
    if data['topic'] == "temperature" :
        print("Message received on topic: " + data["topic"] + " with the message: " + data["payload"])
        socketio.emit('curr_temp', data=data["payload"])
    log_file.write(message)  # Write the message to the log file
    log_file.flush()  # Flush the file to ensure immediate write


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)
    pass

def getIp():
    addresses = netifaces.ifaddresses("enp0s8")
    ip_address = addresses[netifaces.AF_INET][0]['addr']
    return ip_address

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)

    