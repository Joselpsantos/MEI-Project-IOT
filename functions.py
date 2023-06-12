import config
import machine
import network
#from machine import Pin
import utime
from umqtt.simple import MQTTClient

# Inicializar o LED
onboard_led = machine.Pin("LED", machine.Pin.OUT)
led_status = False


# Função para obter o status do LED
def get_led_status():
    return "ligado" if led_status else "desligado"

# Scan de redes Wi-Fi
def get_available_networks():
    wlan = network.WLAN(network.STA_IF)
    networks = wlan.scan()
    return [net[0].decode() for net in networks]

# Reiniciar a RpPW
def machine_reset():
    utime.sleep(1)
    print("Reiniciando...")
    machine.reset()

# Ligar rega
def rega_on():
    print("Executando código ON")

# Desligar rega
def rega_off():
    print("Executando código OFF")

# Função para rega automática
def rega_auto(request):
    temperature = request.query.get("temperature", "")  # Obter a temperatura

    # Verificar se a temperatura é um valor válido
    if temperature.isdigit():
        # Converter a temperatura para o tipo adequado e realizar a ação necessária
        temperature = int(temperature)

        # Exemplo de ação: imprimir a temperatura no console
        print(f"Temperatura definida para: {temperature} graus")

        # Retornar uma resposta de sucesso
        return "OK"
    else:
        # Se a temperatura não for válida, retornar um erro
        return "Temperatura inválida.", 400


#
client_id="picow"
mqtt_server="192.168.8.60"
topic_sub="led"

#
def sub_cb(topic, msg):
    print("New message on topic: {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        led.on()
    elif msg == "off":
        led.off()
        
#
def mqtt_connect():
    client = MQTTClient(client_id,  mqtt_server, port=1883, keepalive=60, user="pico", password="pico")
    client.set_callback(sub_cb)
    client.connect()
    print('Conectado ao %s MQTT Broker'%(mqtt_server))
    return client

#
def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

#

