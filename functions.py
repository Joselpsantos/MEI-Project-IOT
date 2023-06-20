import config
import machine
import network
import json
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import utime
from umqtt.simple import MQTTClient

# Inicializar o LED
onboard_led = machine.Pin("LED", machine.Pin.OUT)
led_status = False

# Definir o pin do relay
relay1=Pin(18,Pin.OUT)
relay2=Pin(19,Pin.OUT)

# Configuração do LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Função para obter o status do LED
def get_led_status():
    return "ligado" if led_status else "desligado"

# Scan de redes Wi-Fi
def get_available_networks():
    wlan = network.WLAN(network.STA_IF)
    networks = wlan.scan()
    return [net[0].decode() for net in networks]

# Ler temperatura
def read_temp():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.2f}".format(temperature)
    string_temperature = str("Temp:" + formatted_temperature)
    print(string_temperature)
    lcd.move_to(0,0)
    lcd.putstr(string_temperature)
    return string_temperature


# Reiniciar a RpPW
def machine_reset():
    utime.sleep(1)
    print("Reiniciando...")
    machine.reset()

# Ligar rega
def rega_on():
    lcd.move_to(0, 1)
    lcd.putstr("Rega ligada   ") # derivado a ter menos caracteres que o desligado
    print("Sistema de rega ligado!")
    #client.publish("Rega", "Ligado")
    #relay1.value(0)

# Desligar rega
def rega_off():
    lcd.move_to(0, 1)
    lcd.putstr("Rega desligada")
    print("Sistema de rega desligado!")
    #client.publish("Rega", "Desligado")
    #relay1.value(1)

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
    #client.publish("Rega", "Automático")

####### MQTT #######
    
client_id="picow"
topic_sub="rega"

#
def sub_cb(topic, msg):
    print("New message on topic: {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        rega_on()
    elif msg == "off":
        rega_off()
    elif msg == "auto":
        rega_auto()
#
def mqtt_connect():
    # Ler as informações do ficheiro conf.json
    with open(config.MQTT_CONFIG_FILE) as f:
        conf_data = json.load(f)

    # Obter as informações do MQTT Server, usuário e senha do arquivo conf.json
    mqtt_server = conf_data.get("mqtt_server", "")
    mqtt_user = conf_data.get("mqtt_user", "")
    mqtt_password = conf_data.get("mqtt_password", "")

    # Criar e configurar o cliente MQTT
    client = MQTTClient(client_id, mqtt_server, port=1883, keepalive=60, user=mqtt_user, password=mqtt_password)
    client.set_callback(sub_cb)
    client.connect()
    print('Conectado ao %s MQTT Broker' % mqtt_server)
    return client

#
def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

#

