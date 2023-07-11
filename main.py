# importar bibliotecas
from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.template import render_template
from picozero import pico_temp_sensor, pico_led
import json
import os
import utime
import _thread
import umail
import config
import functions
import usocket as socket
import network
import uasyncio as asyncio


# Entrar no modo de configuração para definir SSID e senha do Wi-Fi
def setup_mode():
    print("Configurando...")

    def ap_index(request):
        if request.headers.get("host") != config.AP_DOMAIN:
            return render_template(f"{config.AP_TEMPLATE_PATH}/redirect.html", domain=config.AP_DOMAIN)

        networks = functions.get_available_networks()  # Função para obter as redes disponíveis
        print(networks)

        options = ""
        for network in networks:
            options += f'<option value="{network}">{network}</option>'

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1 charset=utf-8"">
            <title>Raspberry Pi Pico W</title>
        </head>
        <body>
            <h1>Configurar rede Wi-Fi</h1>
            <p>Introduza os dados da rede à qual deseja se conectar:</p>
            <form action="/configure" method="POST" autocomplete="off" autocapitalize="none">
                <label for="ssid">SSID:</label><br>
                <select id="ssid" name="ssid">
                    {options}
                </select><br>

                <label for="password">Senha:</label><br>
                <input type="password" id="password" name="password"><br><br>
                <button type="submit">Guardar</button>
            </form>
        </body>
        </html>
        """

        return html_content

    # Guardar as definições do wifi no ficheiro json
    def ap_configure(request):
        print("Guardando configurações...")

        with open(config.WIFI_FILE, "w") as f:
            json.dump(request.form, f)
            f.close()

        # Reiniciar PicoW
        _thread.start_new_thread(functions.machine_reset, ())
        return render_template(f"{config.AP_TEMPLATE_PATH}/configured.html", ssid=request.form["ssid"])

    def ap_catch_all(request):
        if request.headers.get("host") != config.AP_DOMAIN:
            return render_template(f"{config.AP_TEMPLATE_PATH}/redirect.html", domain=config.AP_DOMAIN)

        return "Not found.", 404

    # Rotas definidas na configuração do RPicoW
    server.add_route("/", handler=ap_index, methods=["GET"])
    server.add_route("/configure", handler=ap_configure, methods=["POST"])
    server.set_callback(ap_catch_all)

    ap = access_point(config.AP_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)

# Após sucesso na ligação ao wifi, o RpicoW entra no modo "aplicação"
def application_mode(client):
    # O WebServer agora está ativo
    print("Modo Web Ativo.")

    def app_index(request):
        ip_address = connect_to_wifi(wifi_credentials["ssid"], wifi_credentials["password"])
        temperatura = str(pico_temp_sensor.temp)
        html_content = render_template(f"{config.APP_TEMPLATE_PATH}/index.html", temperature=temperatura, rega_status=functions.get_led_status())
        return html_content

    def app_toggle_led(request):
        functions.toggle_led()
        return app_index(request)

    def app_rega_on(request):
        functions.rega_on(client)
        return "ok"

    def app_rega_off(request):
        functions.rega_off(client)
        return "ok"

    def app_rega_auto(request):
        loop = functions.asyncio.get_event_loop()
        loop.create_task(functions.rega_auto(request, client))
        loop.run_forever()

        return "ok"
    
    def lcd_update_thread():
        while True:
            functions.read_temp_lcd() # Envia a temperatura para o LCD
            try:
                client.publish("temperature", functions.read_temp()) # Envia a temperatura para o broker
            except Exception as e:
                pass
            utime.sleep(10) # Aguarda 10 segundos

    # Página de configuração do MQTT
    def render_mqtt_config_page(mqtt_server="", mqtt_user="", mqtt_password="", mqtt_topic="", temprega=""):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Configurações RPicoW</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
        </head>
        <body>
            <div class="container">
                <h2 class="mt-4">Configurações MQTT</h2>
                <form action="/config" method="POST">
                    <div class="form-group">
                        <label for="mqttServer">Servidor MQTT:</label>
                        <input type="text" class="form-control" id="mqttServer" name="mqttServer" placeholder="Endereço do servidor MQTT" value="{mqtt_server}">
                    </div>

                    <div class="form-group">
                        <label for="mqttUser">Utilizador MQTT:</label>
                        <input type="text" class="form-control" id="mqttUser" name="mqttUser" placeholder="Utilizador MQTT" value="{mqtt_user}">
                    </div>

                    <div class="form-group">
                        <label for="mqttPassword">Senha MQTT:</label>
                        <input type="password" class="form-control" id="mqttPassword" name="mqttPassword" placeholder="Senha MQTT">
                    </div>

                    <div class="form-group">
                        <label for="mqttTopic">Tópico Subscrito:</label>
                        <input type="text" class="form-control" id="mqttTopic" name="mqttTopic" placeholder="Tópico subscrito" value="{mqtt_topic}">
                    </div>
                    
                    <h2 class="mt-4">Outras configurações</h2>
                    <div class="form-group">
                        <label for="emprega">Tempo de Rega:</label>
                        <input type="text" class="form-control" id="temprega" name="temprega" placeholder="Segundos de Rega" value="{temprega}">
                    </div>
                    
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="deleteWifiConfig">
                        <label class="form-check-label" for="deleteWifiConfig">Apagar configuração Wi-Fi</label>
                    </div>

                    <button onclick="window.location.href='/'" class="btn btn-primary mt-3">Voltar</button>
                    <button type="submit" class="btn btn-primary mt-3">Guardar</button>
                </form>
            </div>
        </body>
        </html>
        """

        return html_content.format(mqtt_server=mqtt_server, mqtt_user=mqtt_user, mqtt_password=mqtt_password, mqtt_topic=mqtt_topic, temprega=temprega)

    # configuração do MQTT
    def app_mqtt_config(request):
        if request.method == "GET":
            try:
                # Verificar se o ficheiro conf.json
                os.stat(config.MQTT_CONFIG_FILE)

                # Ler as informações do ficheiro conf.json
                with open(config.MQTT_CONFIG_FILE) as f:
                    conf_data = json.load(f)

                # Renderizar a página de configurações MQTT com os valores existentes
                mqtt_server = conf_data.get("mqtt_server", "")
                mqtt_user = conf_data.get("mqtt_user", "")
                mqtt_password = conf_data.get("mqtt_password", "")
                mqtt_topic = conf_data.get("mqtt_topic", "")
                temprega = conf_data.get("temprega", "")
                html_content = render_mqtt_config_page(mqtt_server=mqtt_server, mqtt_user=mqtt_user, mqtt_password=mqtt_password, mqtt_topic=mqtt_topic, temprega=temprega)
            except OSError:
                # Renderizar a página de configurações MQTT sem valores
                html_content = render_mqtt_config_page()
            
            return html_content

        elif request.method == "POST":
            # Ler os dados do formulário POST
            mqtt_server = request.form.get("mqttServer")
            mqtt_user = request.form.get("mqttUser")
            mqtt_password = request.form.get("mqttPassword")
            mqtt_topic = request.form.get("mqttTopic")
            temprega = request.form.get("temprega")

            # Validar e guardar as configurações
            if mqtt_server and mqtt_user and mqtt_topic:
                conf_data = {
                    "mqtt_server": mqtt_server,
                    "mqtt_user": mqtt_user,
                    "mqtt_password": mqtt_password,
                    "mqtt_topic": mqtt_topic,
                    "temprega": temprega
                }

                # Salvar as informações no arquivo conf.json
                with open(config.MQTT_CONFIG_FILE, "w") as f:
                    json.dump(conf_data, f)

                return "Configurações MQTT guardadas com sucesso!"
            else:
                return "Erro a guardar as configurações MQTT!"

    def app_catch_all(request):
        return "Not found.", 404
    
    # Definir as rotas
    server.add_route("/", handler=app_index, methods=["GET"])
    server.add_route("/toggle", handler=app_toggle_led, methods=["GET"])
    
    server.add_route("/on", handler=app_rega_on, methods=["GET"])
    server.add_route("/off", handler=app_rega_off, methods=["GET"])
    server.add_route("/auto", handler=app_rega_auto, methods=["GET"])
    server.add_route("/config", handler=app_mqtt_config, methods=["GET", "POST"])
    # server.add_route("/log", handler=app_log, methods=["GET"])
    # Adicionar outras rotas
    
    server.set_callback(app_catch_all)
    
    # Inicia o while do lcd
    _thread.start_new_thread(lcd_update_thread, ())
    

try:
    os.stat(config.WIFI_FILE)

    # Arquivo encontrado e conectar ao Wi-Fi
    with open(config.WIFI_FILE) as f:
        wifi_credentials = json.load(f)
        ip_address = connect_to_wifi(wifi_credentials["ssid"], wifi_credentials["password"])

        if not is_connected_to_wifi():
            # Conexão ruim. Remover arquivo
            print("Dificuldades a ligar ao Wi-Fi!")
            print(wifi_credentials)
            os.remove(config.WIFI_FILE)
            functions.machine_reset()

        print(f"Conectado ao Wi-Fi com o IP: {ip_address}")

        # Enviar e-mail com o endereço IP do PicoW
        #smtp = umail.SMTP(config.smtp_server, 465, ssl=True)
        #smtp.login(config.sender_email, config.sender_app_password)
        #smtp.to(config.recipient_email)
        #smtp.write("From:" + config.sender_name + "<" + config.sender_email + ">\n")
        #smtp.write("Subject:" + ip_address + "\n")
        #status_code, response = smtp.send()
        #if status_code == 250:
        #    print("Email enviado com sucesso!")
        #else:
        #    print("Falha no envio do email. Erro:", response)
        #smtp.quit()

                
        # Ligar ao Broker MQTT
        try:
            print("A tentar ligar ao Broker MQTT...")
            client = functions.mqtt_connect()

        except Exception as e:
            print("Erro ao conectar e subscrever ao broker MQTT:", e)
            _thread.start_new_thread(functions.machine_reset, ())
                #.reconnect()

        # Entra no modo da aplicação     
        application_mode(client)
        
        
        def start_mqtt_listener(client):
            loop = functions.asyncio.get_event_loop()
            loop.create_task(functions.mqtt_listener(client))
            loop.run_forever()
            
        def read_conf_file():
            with open("conf.json", "r") as file:
                conf_data = json.load(file)
            return conf_data

        conf_data = read_conf_file()

        subscribe_mode = conf_data.get("subscribe_mode", "")

        if subscribe_mode == "ON":
            start_mqtt_listener(client)
        elif subscribe_mode == "OFF":
            pass    
            
        
except Exception:
    # Se não encontrar as credenciais do Wi-Fi, inicia o modo de configuração
    setup_mode()

# Iniciar o WebServer
server.run()
