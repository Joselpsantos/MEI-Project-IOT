 
# Projeto IOT
Criação de um sistema de rega, acente na placa de desenvolvimento Raspberry Pico W (doravante denoinado de "RPW"), onde foi implementado Captive Portal para efetuar a ligação do RPW à rede WI-FI, e posterior configuração do broker num servidor WEB instalado na propria memória.
Foi desenvolvido também, em Flask, um portal de gestão utilizando Websockets.



# Índice  
1. [Introdução](#projeto-mqtt-broker)    
3. [Características](#Características) 
4. [Recursos utilizados](#o-que-aprendi)
5. [Iniciar o projeto](#iniciar-o-projeto)
6. [Variáveis](#variáveis)
7. [Comandos úteis](#comandos-úteis)
7. [Relatório](#relatório)
8. [Bibliografia](#Bibliografia)
9. [Licença](#Licença)


## Screenshots  

![App Screenshot](https://github.com/Joselpsantos/MEI-Project-IOT/assets/113514374/31623f6e-d969-471d-90da-f9c6999aba5e)

## Recursos utilizado  

**Software:** 
- microPhyton
- VirtualBox/Vagrant
- Broker Mosquitto MQTT
- VSCODE
- Thonny  

**Hardware:** 
- 1x Raspberry Pico W (doravante denominado de RPW)
- 1x Relay 2 canais
- 2x LED
- 1x LCD duas linhas 
- 5x resistências

## Características  

VM´s:
- Instalação e configuração automática da VM   
- Instalação e configuração do broker Mosquitto  
- Instalação e configuração do flask com WebSockets ("WS") 

Raspberry Pico w:
- Ligar ao wireless com captive portal
- Ligação ao broker feita em página dedicada
- Envio da temperatura para o Broker
- Receção de instrução para Ligar/desligar a Rega, ou colocação em modo automático, defenindo a partir de que temperatura deverá ligar 

## Iniciar o projeto 

Clonar o projeto  

~~~bash  
  git clone https://github.com/PaivaX/MQTT-vagrant.git
~~~

Ir para o diretório do projeto  

~~~bash  
  cd vagrant-mqtt
~~~

Iniciar as VM  

~~~bash  
vagrant up
~~~

## Variáveis  

Definir o user e password, no ficheiro "install_mosquitto.sh":  
`user`

`password`  

Para alterar o tópico, deve ser alterado no ficheiro mqtt_sub.py

`topic` 


## Comandos úteis

Entrar no SSH da VM.
~~~bash 
vagrant ssh <nome_vm>
~~~

Iniciar VM

~~~bash
vagrant up <nome_vm>
~~~

Desligar VM

~~~bash
vagrant halt
~~~~

Destruir VM. O código-fonte e o conteúdo do diretório de dados permanecerão inalterados. 
Somente a instância da máquina VirtualBox será destruída. Pode-se construir a VM com o comando 'vagrant up'.


~~~bash 
vagrant destroy
~~~

Reconfigurar VM depois de alterações ao código fonte.
~~~bash
vagrant provision
~~~

Recarregar VM. Útil quando se altera as propriedades de rede.
~~~bash$
vagrant reload
~~~

## Relatório  

Objetivo do projeto:

Configurar um dispositivo IOT, por forma a criar um sistema automatizado, e com ligação a um broker MQTT, sendo que teria de possuir um sistema de autenticação na rede WIFI, e uma condição de automação e funcionamento.


Hardware utilizado:
 

Programa utilizado:

Para desenvolver o programa em Python (Microphtyon), que vai ser executado no RPW, recorremos ao software <b>Thonny</b>.


Este é um código Python que consiste em dois ficheiros principais: main.py e functions.py. 

Iremos descrever cada um deles em detalhe:

main.py - ficheiro responsável pela execução do código de inicialização:

Importações:

<b>config</b>: módulo personalizado que contém algumas configurações do programa desenvolvido.

<b>machine</b>: módulo para controlo do hardware do RPW.

<b>network</b>: módulo para configuração e gestão de redes.

<b>json</b>: módulo para trabalhar com JSON.

<b>I2C, Pin</b>: classes do módulo machine para controle de I2C e pinos.

<b>LcdApi, I2cLcd</b>: classes para controlar um display LCD via I2C.

<b>utime</b>: módulo para trabalhar com tempo.

<b>_thread</b>: módulo para suporte a threads.

<b>micropython</b>: módulo com funções específicas do Micropython.

<b>MQTTClient</b>: classes para criar um cliente MQTT.

<b>uasyncio</b>: biblioteca para programação assíncrona no Micropython.

#### Inicialização de conexões:

onboard_led, led_r, led_g, led_b: pinos de LED utilizados.

led_status, lcd_connected: variáveis de estado para o LED e o LCD.

temperature, sensor_temp, conversion_factor: variáveis relacionadas à leitura de temperatura usando o sensor interno

I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS: constantes para configurar o LCD.

Verificação da conexão do LCD:

Tenta inicializar o objeto lcd do tipo I2cLcd para se comunicar com o LCD.
Define a variável lcd_connected como True se a inicialização for bem-sucedida, caso contrário, False. Foi criado esta verificação, para o caso do LCD estar desligado.

#### Definição das funções de controle das cores do LED:

<b>led_red(), led_green(), led_blue()</b>: funções para definir a cor do LED acendendo ou apagando os pinos R, G e B.

<b>Função get_led_status()</b>: retorna o status atual do LED como uma string ("ligado" ou "desligado").

<b>Função get_available_networks()</b>: verifica as redes Wi-Fi disponíveis e retorna uma lista dos SSIDs.

<b>Função check_temp()</b>: realiza a leitura do sensor de temperatura analógico e converte o valor em temperatura Celsius.

<b>Função read_temp()</b>: lê a temperatura atual e retorna uma string.

<b>Função read_temp_lcd()</b>: exibe a temperatura atual no LCD se estiver conectado.

<b>Função machine_reset()</b>: reinicia o Raspberry Pi Pico.

<br>
<b>Configuração do MQTT</b>:

<b>topic_sub, topic</b>: tópicos MQTT para assinatura e controle.

<b>sub_cb()</b>: função de callback para tratar mensagens MQTT recebidas.

<b>mqtt_connect()</b>: realiza a conexão com o servidor MQTT e retorna o objeto MQTTClient.

<b>reconnect()</b>: função para reconectar ao servidor MQTT em caso de falha na conexão.

<b>rega_on(), rega_off()</b>: funções para ligar e desligar a rega.

<b>rega_auto()</b>: função para executar o modo de rega automática com base na temperatura.

<b>update_conf_file()</b>: atualiza o ficheiro de configuração MQTT.

<b>mqtt_listener()</b>: função assíncrona para ouvir as mensagens MQTT.


### Conexão com o WI-FI
```
  if not is_connected_to_wifi():
    # Conexão ruim. Remover arquivo
    print("Dificuldades a ligar ao Wi-Fi!")
    print(wifi_credentials)
    os.remove(config.WIFI_FILE)
    functions.machine_reset()
```



Verifica se existe um ficheiro de configuração do Wi-Fi. Se existir, tenta conectar ao Wi-Fi e iniciar o cliente MQTT. Caso contrário, entra no modo de configuração do Wi-Fi.


### Definir as rotas
    server.add_route("/", handler=app_index, methods=["GET"])
    server.add_route("/toggle", handler=app_toggle_led, methods=["GET"])
    
    server.add_route("/on", handler=app_rega_on, methods=["GET"])
    server.add_route("/off", handler=app_rega_off, methods=["GET"])
    server.add_route("/auto", handler=app_rega_auto, methods=["GET"])
    server.add_route("/config", handler=app_mqtt_config, methods=["GET", "POST"])
    # server.add_route("/log", handler=app_log, methods=["GET"])
    # Adicionar outras rotas


Define rotas e controladores de solicitações HTTP.
Inicializa uma thread separada para atualizar o LCD com a temperatura atual.
Bloco try-except para verificar se o ficheiro de configuração MQTT existe.

Se existir, verifica o modo de inscrição e inicia uma thread separada para ouvir as mensagens MQTT.
Bloco final para iniciar o servidor web.
 

# functions.py:

Importações:

phew, pico_temp_sensor, pico_led, json, os, utime, _thread, umail, config, usocket as socket, network, uasyncio as asyncio.
setup_mode(): função para entrar no modo de configuração do Wi-Fi.

application_mode(client): função para executar o modo de aplicação após a conexão bem-sucedida ao Wi-Fi.

Define rotas e controladores de solicitações HTTP para a aplicação.
Inicializa uma thread separada para atualizar o LCD com a temperatura atual.
Essas são as principais funcionalidades e estrutura do código fornecido. Ele lida com a leitura de temperatura, controle de LED, comunicação MQTT, configuração de Wi-Fi e servidor web para controlar um sistema de rega.
 
No main.py:

Importações: Importa os módulos necessários para o funcionamento do código.

Inicialização de conexões: Define as conexões, como pinos de LED e configurações do LCD.
Verificação da conexão do LCD: Verifica se o LCD está conectado corretamente.
Definição das funções de controle das cores do LED: Define funções para controlar as cores do LED.
Função get_led_status(): Retorna o status atual do LED.

<b>Função get_available_networks()</b>: Retorna a lista de redes Wi-Fi disponíveis.

<b>Função check_temp()</b>: Lê a temperatura atual usando um sensor analógico.

<b>Função read_temp()</b>: Lê a temperatura atual e retorna uma string formatada.

<b>Função read_temp_lcd()</b>: Exibe a temperatura no LCD, se estiver conectado.

<b>Função machine_reset()</b>: Reinicia o Raspberry Pi Pico.

<b>Configuração do MQTT</b>: Define as configurações relacionadas ao MQTT, como tópicos, funções de callback e conexão.

Bloco try-except: Verifica se existe um ficheiro de configuração do Wi-Fi e inicia o cliente MQTT.

application_mode(): Executa o modo de aplicação após a conexão bem-sucedida ao Wi-Fi. Define rotas e controladores de solicitações HTTP.

Bloco try-except para verificar se o ficheiro de configuração MQTT existe. Inicia uma thread separada para ouvir as mensagens MQTT.
Bloco final para iniciar o servidor web.

#### functions.py:

Importações: Importa os módulos e pacotes necessários para o funcionamento do código.
setup_mode(): Entra no modo de configuração do Wi-Fi, onde o usuário pode fornecer as informações de SSID e senha.

application_mode(client): Executa o modo de aplicação após a conexão bem-sucedida ao Wi-Fi. Define rotas e controladores de solicitações HTTP para a aplicação.


Essas são as principais partes do código e o que cada função faz. Cada função desempenha um papel específico no controlo do sistema de rega, comunicação MQTT, atualização do LCD, configuração do Wi-Fi, e do controlo dos LEDs.


#### FLASK - Painel de controlor


## Funcionamento

## Dificuldades
Uma vez que para este projeto foi utilizado o Raspberry Pico W, que é um hardware excelente custo vs benefícios, contudo, para projetos mais elaborados, as suas caracteristicas/recursos ficam limitados.

Na execução deste projeto, utilizámos um LCD, uma ligação AP, e um broker, o que se revelou claramente exigente para o hardware.
Para contornar o problema constante de esgotar os recursos, tivemos de procurar soluções alternativas, pelo que fizemos uso de threads, e de funções assíncronas.
Mesmo utilizando estas tecnologias 

## Bibliografia  

- [Peppe8o](https://peppe8o.com/mqtt-and-raspberry-pi-pico-w-start-with-mosquitto-micropython/)
- [Steve´s Internet Guide](http://www.steves-internet-guide.com/mqtt/)
- [Tomshardware](https://www.tomshardware.com/how-to/connect-raspberry-pi-pico-w-to-the-internet)
