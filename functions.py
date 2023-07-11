import config
import machine
import network
import json
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import utime
import _thread
import micropython
from umqtt.simple import MQTTClient
import uasyncio as asyncio

# Inicializar ligações
onboard_led = machine.Pin("LED", machine.Pin.OUT)
led_r = Pin(18, Pin.OUT)
led_g = Pin(14, Pin.OUT)
led_b = Pin(2, Pin.OUT)
# Definir o pin do relay
#relay1=Pin(1,Pin.OUT)
#relay2=Pin(19,Pin.OUT)

# Status de arranque
led_status = False
lcd_connected = False
led_r.value(1)
led_g.value(1)
led_b.value(1)

# Leitura da temperatura
temperature = 0
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
        
# Configuração do LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)

# Verifica se o LCD está ligado
try:
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    lcd_connected = True
except:
    lcd_connected = False

# Definir as cores
def led_red():
    led_r.value(0)
    led_g.value(1)
    led_b.value(1)
    
def led_green():
    led_r.value(1)
    led_g.value(0)
    led_b.value(1)
    
def led_blue():
    led_r.value(1)
    led_g.value(1)
    led_b.value(0)
    
# Função para obter o status do LED
def get_led_status():
    return "ligado" if led_status else "desligado"

# Scan de redes Wi-Fi
def get_available_networks():
    wlan = network.WLAN(network.STA_IF)
    networks = wlan.scan()
    return [net[0].decode() for net in networks]

# Função para verificar a temperatura
def check_temp():
    reading = sensor_temp.read_u16() * conversion_factor 
    current_temperature = 27 - (reading - 0.706) / 0.001721
    return current_temperature

# Ler temperatura
def read_temp():
    temperature = check_temp()
    formatted_temperature = "{:.2f}".format(temperature)
    string_temperature = str("Temp:" + formatted_temperature)

    return string_temperature

# Ler temperatura para imprimmir no LCD
def read_temp_lcd():  
    if lcd_connected:
        print(read_temp())
        lcd.move_to(0,0)
        lcd.putstr(read_temp())
    else:
        pass
        
# Reiniciar a RpPW
def machine_reset():
    utime.sleep(1)
    print("Reiniciando...")
    machine.reset()

####### MQTT #######
    
topic_sub="rega"
topic="control"

# Subscribe
def sub_cb(topic, msg, client):
    print("New message on topic: {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        rega_on(client)
    elif msg == "off":
        rega_off(client)
    elif msg.startswith("\"AUTO\","):
        try:
            temperature = int(msg.split(",")[1])
            #rega_auto(temperature, client)
            loop = asyncio.get_event_loop()
            loop.create_task(rega_auto(request, client, temperature))
            loop.run_forever()
        except (ValueError, IndexError):
            print("Formato inválido da mensagem AUTO")
        
# Conexão MQTT
def mqtt_connect():
    # Ler as informações do ficheiro conf.json
    with open(config.MQTT_CONFIG_FILE) as f:
        conf_data = json.load(f)

    # Obter as informações do MQTT Server, usuário e senha do arquivo conf.json
    mqtt_server = conf_data.get("mqtt_server", "")
    mqtt_user = conf_data.get("mqtt_user", "")
    mqtt_password = conf_data.get("mqtt_password", "")

    # Criar e configurar o cliente MQTT
    client = MQTTClient("picoW", mqtt_server, port=1883, keepalive=60, user=mqtt_user, password="pico")
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe("control")
    
    print('Conectado ao %s MQTT Broker' % mqtt_server)
        
    return client

    
# Reconectar ligação ao MQTT Broker
def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    utime.sleep(5)
    machine.reset()

# Ligar rega
def rega_on(client):
    #client = mqtt_connect()
    with open(config.MQTT_CONFIG_FILE) as f:
        conf_data = json.load(f)
    mqtt_topic = conf_data.get("mqtt_topic")
    if lcd_connected:
        lcd.clear()
        lcd.move_to(0, 1)
        lcd.putstr("Rega ligada") # derivado a ter menos caracteres que o desligado
    with open("auto.txt", "w") as f:
        f.write("ON")
        print(f"Estado pretendido salvo: ON")
    print("Sistema de rega ligado!")
    client.publish(mqtt_topic, "Ligado")
    led_green()
    #relay1.value(0)

# Desligar rega
def rega_off(client):
    #client = mqtt_connect()
    with open(config.MQTT_CONFIG_FILE) as f:
        conf_data = json.load(f)
    mqtt_topic = conf_data.get("mqtt_topic")
    if lcd_connected:
        lcd.move_to(0, 1)
        lcd.putstr("Rega desligada")
    with open("auto.txt", "w") as f:
        f.write("OFF")
        print(f"Estado pretendido salvo: OFF")
    print("Sistema de rega desligado!")
    client.publish(mqtt_topic, "Desligado")
    led_red()
    #relay1.value(1)

async def rega_auto(request, client):
    led_blue()
    with open(config.MQTT_CONFIG_FILE) as f:
        conf_data = json.load(f)
    mqtt_topic = conf_data.get("mqtt_topic")
    temperature = request.query.get("temperature", "")  # Obter a temperatura
    
    # Envia o estado para o LCD
    if lcd_connected:
        lcd.clear()
        lcd.move_to(0, 1)
        lcd.putstr("Rega AUTO")
        
    # Envia msg MQTT
    client.publish(mqtt_topic, "AUTO")
        
    def get_temperature():
        sensor_temp = machine.ADC(4)
        conversion_factor = 3.3 / (65535)
        reading = sensor_temp.read_u16() * conversion_factor 
        temperature = 27 - (reading - 0.706)/0.001721
        return temperature
    
    # Verificar se a temperatura é um valor válido
    if temperature.isdigit():
        # Converter a temperatura para INT
        temperature = int(temperature)

        # Imprimir a temperatura na consola
        #print(f"Temperatura definida para: {temperature} graus")
        
        # Escrever o estado pretendido em um arquivo
        with open("auto.txt", "w") as f:
            f.write(f'"AUTO",{temperature}')
            print(f"Estado pretendido guardado: AUTO. Temperatura: {temperature}")
        
        while True:
            if get_temperature() >= temperature:
                # Ativar a rega
                rega_on(client)
                print(get_temperature())
                await asyncio.sleep(40)  # Aguardar 5 minutos
                rega_off(client)
            else:
                await asyncio.sleep(10)  # Aguardar 10 segundos antes de verificar novamente
            
        # Retornar uma resposta de sucesso
        return "OK"
    else:
        # Se a temperatura não for válida, retornar um erro
        return "Temperatura inválida.", 400
    client.publish("Rega", "Automático")

def update_conf_file(client):
    with open(config.MQTT_CONFIG_FILE, "r") as f:
        conf_data = json.load(f)
    conf_data["subscribe_mode"] = "OFF"
    with open(config.MQTT_CONFIG_FILE, "w") as f:
        json.dump(conf_data, f)
        
async def mqtt_listener(client):
    def mqtt_callback(topic, msg):
        #print("Mensagem recebida no tópico:", topic)
        print("Mensagem recebida:", msg.decode())
        msg = msg.decode('utf-8')
        print(msg)
        if msg == "on":
            rega_on(client)
        elif msg == "off":
            rega_off(client)
        elif msg == "auto":
            rega_auto(client)
        elif msg == "unsubscribe":
            update_conf_file(client)

    #
    client.set_callback(mqtt_callback)
    client.subscribe("control")

    while True:
        await asyncio.sleep(1)  # Aguarda 1 segundo para evitar bloqueio

        try:
            client.check_msg()  # Verifica se há mensagens recebidas
        except Exception as e:
            print("Erro na verificação de mensagens MQTT:", e)

