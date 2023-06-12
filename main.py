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

    server.add_route("/", handler=ap_index, methods=["GET"])
    server.add_route("/configure", handler=ap_configure, methods=["POST"])
    server.set_callback(ap_catch_all)

    ap = access_point(config.AP_NAME)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)

def application_mode():
    # O WebServer agora está ativo
    print("Modo Web Ativo.")
    
    def app_index(request):
        ip_address = connect_to_wifi(wifi_credentials["ssid"], wifi_credentials["password"])
        temperatura = str(pico_temp_sensor.temp)
        html_content = render_template(f"{config.APP_TEMPLATE_PATH}/index.html", temperature=temperatura, led_status=functions.get_led_status())
        return html_content

    def app_toggle_led(request):
        functions.toggle_led()
        return app_index(request)
    
    def app_rega_on(request):
        functions.rega_on()
        client.publish("Rega", "Ligado")
        return "ok"
    
    def app_rega_off(request):
        functions.rega_off()
        client.publish("Rega", "Desligado")
        return "ok"
   
    def app_rega_auto(request):
        functions.rega_auto(request)
        client.publish("Rega", "Automático")
        return "ok"
    
    def app_mqtt_config(request):
        try:
            # Verificar se o ficheiro conf.json existe
            os.stat(config.MQTT_CONFIG_FILE)

            # Ler as informações do ficheiro conf.json
            with open(config.MQTT_CONFIG_FILE) as f:
                conf_data = json.load(f)
                mqtt_server = conf_data.get("mqtt_server", "")
                mqtt_user = conf_data.get("mqtt_user", "")
                mqtt_password = conf_data.get("mqtt_password", "")
                mqtt_topic = conf_data.get("mqtt_topic", "")
                f.close()
        except Exception:
            # Definir as informações como vazias
            mqtt_server = ""
            mqtt_user = ""
            mqtt_password = ""
            mqtt_topic = ""


        # Renderizar o template com as informações MQTT
        html_content = render_template(f"{config.APP_TEMPLATE_PATH}/config-mqtt.html",
                                       mqtt_server=mqtt_server,
                                       mqtt_user=mqtt_user,
                                       mqtt_password=mqtt_password,
                                       mqtt_topic=mqtt_topic)
        return html_content
        
    def app_mqtt_config_ok(request):
        # Obter os valores dos campos do formulário
        mqtt_server = request.form("mqttServer")
        mqtt_user = request.form("mqttUser")
        mqtt_password = request.form("mqttPassword")
        mqtt_topic = request.form("mqttTopic")

        # Criar um dicionário com as credenciais MQTT
        mqtt_credentials = {
            "mqtt_server": mqtt_server,
            "mqtt_user": mqtt_user,
            "mqtt_password": mqtt_password,
            "mqtt_topic": mqtt_topic
        }
        
        #Verificar se está a receber as informações do site
        print(f"MQTT Server: {mqtt_server}")
        print(f"MQTT User: {mqtt_user}")
        print(f"MQTT Password: {mqtt_password}")
        print(f"MQTT Topic: {mqtt_topic}")
        
        try:
            # Guarda as credenciais em um ficheiro
            with open(config.MQTT_CONFIG_FILE, "w") as f:
                json.dump(mqtt_credentials, f)
        except Exception as e:
            # Erro de gravação
            error_message = "Erro ao gravar as credenciais MQTT. Por favor, tente novamente mais tarde."
            # Aqui você pode registrar o erro, exibir uma mensagem de erro ao usuário, redirecionar para uma página de erro, etc.
            # Por simplicidade, vamos retornar uma resposta com a mensagem de erro.
            return error_message

        # Renderizar o template com as informações MQTT
        return "OK"


    def app_catch_all(request):
        return "Not found.", 404

    server.add_route("/", handler=app_index, methods=["GET"])
    server.add_route("/toggle", handler=app_toggle_led, methods=["GET"])
    # Adicionar outras rotas
    server.add_route("/on", handler=app_rega_on, methods=["GET"])
    server.add_route("/off", handler=app_rega_off, methods=["GET"])
    server.add_route("/auto", handler=app_rega_auto, methods=["GET"])
    server.add_route("/config", handler=app_mqtt_config, methods=["GET"])
    server.add_route("/config/ok", handler=app_mqtt_config_ok, methods=["POST"])
    #server.add_route("/log", handler=app_log, methods=["GET"])


    server.set_callback(app_catch_all)

try:
    os.stat(config.WIFI_FILE)

    # Arquivo encontrado e conectar ao Wi-Fi
    with open(config.WIFI_FILE) as f:
        wifi_credentials = json.load(f)
        ip_address = connect_to_wifi(wifi_credentials["ssid"], wifi_credentials["password"])

        if not is_connected_to_wifi():
            # Conexão ruim. Remover arquivo
            print("Má conexão Wi-Fi!")
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

        application_mode()
        
        # Ligar ao Broker MQTT
        print("A tentar ligar ao Broker MQTT...")
        try:
            client = functions.mqtt_connect()
        #client.connect()
        #client.subscribe(functions.topic_sub)
        
        except OSError as e:
            print("Erro ao conectar ao broker")
      #      functions.reconnect()

      #      client.check_msg()
      #      time.sleep(1)
        
except Exception:
    # Se não encontrar as credenciais do Wi-Fi, inicie o modo de configuração
    setup_mode()

# Iniciar o WebServer
server.run()
while True:
  client.subscribe(functions.topic_sub)

