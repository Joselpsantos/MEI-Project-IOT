import config
import machine
from machine import Pin
import utime

# Inicializar o LED
onboard_led = machine.Pin("LED", machine.Pin.OUT)
led_status = False

# LED RGB
led_r = Pin(16, Pin.OUT)
led_g = Pin(17, Pin.OUT)
led_b = Pin(15, Pin.OUT)

led_r.value(1)
led_g.value(1)
led_b.value(1)

while True:
    led_r.toggle()
    utime.sleep(1)
    led_r.toggle()

    led_g.toggle()
    utime.sleep(1)
    led_g.toggle()

    # Alteração: Ligar simultaneamente o LED vermelho e verde para obter a cor amarela
    led_r.value(1)
    led_g.value(0)

    utime.sleep(1)
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

