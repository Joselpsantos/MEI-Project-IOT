from flask import Flask, request, jsonify, render_template, redirect
from flask_mqtt import Mqtt
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

app.config['MQTT_BROKER_URL'] = '192.168.45.10'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'pico'  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = 'pico'  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
topic = 'jose'
received_message = ""
led_status = ""
mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
       global received_message
       global led_status
       received_message = ""
       led_status = ""
   else:
       print('Bad connection. Code:', rc)
       
@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):

   global received_message
   global led_status
   msg = message.payload.decode()
   if msg == 'on' or msg == 'off':
      led_status = msg
      #sockets.send(led_status)
      

   else:
      received_message = msg
      #sockets.send(received_message)
      
@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000, debug=True)      
   
@sockets.route('/socket')
def ws_conn(ws):
   while not ws.closed:
      #message = ws.receive()
      ws.send(received_message)  # This is required to keep the WebSocket connection open

@app.route('/')
def home():
   global received_message
   global led_status
   return render_template('index.html', received_message = received_message, led_status = led_status)

@app.route('/something')
def something():
   global received_message
   global led_status
   return render_template('something.html')

@app.route('/LED/ON')
def on():
   mqtt_client.publish(topic, 'on')
   return redirect('/')
   
@app.route('/LED/OFF')
def off():
   mqtt_client.publish(topic, 'off')
   return redirect('/')
   