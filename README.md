 
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

Objetivo do projeto
Vagrant
MQTT




 

Para desenvolver o programa, que vai ser executado no RPW Este é um código Python que consiste em dois arquivos principais: main.py e functions.py. Vou descrever cada um deles em detalhes:

main.py:

Importações:

config: módulo personalizado que contém algumas configurações.

<b>machine</b>: módulo para controle de hardware do Raspberry Pi Pico.

<b>network: módulo para configuração e gerenciamento de redes.

<b>json: módulo para trabalhar com JSON.

<b>I2C, Pin: classes do módulo machine para controle de I2C e pinos.

<b>LcdApi, I2cLcd: classes para controlar um display LCD via I2C.

<b>utime: módulo para trabalhar com tempo.

<b>_thread: módulo para suporte a threads.

<b>micropython: módulo com funções específicas do Micropython.

<b>MQTTClient</b>: classe para criar um cliente MQTT.

<b>uasyncio</b>: biblioteca para programação assíncrona no Micropython.

<b>Inicialização de conexões:</b>

onboard_led, led_r, led_g, led_b: pinos de LED definidos como saída.
led_status, lcd_connected: variáveis de estado para o LED e o LCD.
temperature, sensor_temp, conversion_factor: variáveis relacionadas à leitura de temperatura usando um sensor analógico.

I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS: constantes para configurar o LCD.
i2c: objeto I2C para comunicação com o LCD.
Verificação da conexão do LCD:

Tenta inicializar o objeto lcd do tipo I2cLcd para se comunicar com o LCD.
Define a variável lcd_connected como True se a inicialização for bem-sucedida, caso contrário, False.
Dfinição das funções de controle das cores do LED:

led_red(), led_green(), led_blue(): funções para definir a cor do LED acendendo ou apagando os pinos R, G e B.

Função get_led_status(): retorna o status atual do LED como uma string ("ligado" ou "desligado").

Função get_available_networks(): verifica as redes Wi-Fi disponíveis e retorna uma lista de seus SSIDs.

Função check_temp(): realiza a leitura do sensor de temperatura analógico e converte o valor em temperatura Celsius.

Função read_temp(): lê a temperatura atual e retorna uma string formatada.

Função read_temp_lcd(): exibe a temperatura atual no LCD se estiver conectado.

Função machine_reset(): reinicia o Raspberry Pi Pico.

<b>Configuração do MQTT:</b>

topic_sub, topic: tópicos MQTT para assinatura e controle.

sub_cb(): função de callback para tratar mensagens MQTT recebidas.

mqtt_connect(): realiza a conexão com o servidor MQTT e retorna o objeto MQTTClient.

reconnect(): função para reconectar ao servidor MQTT em caso de falha na conexão.

rega_on(), rega_off(): funções para ligar e desligar a rega.

rega_auto(): função para executar o modo de rega automática com base na temperatura.

update_conf_file(): atualiza o arquivo de configuração MQTT.

mqtt_listener(): função assíncrona para ouvir as mensagens MQTT.

try-except block:

Verifica se existe um arquivo de configuração do Wi-Fi. Se existir, tenta conectar ao Wi-Fi e iniciar o cliente MQTT. Caso contrário, entra no modo de configuração do Wi-Fi.
application_mode(): função para executar o modo de aplicação após a conexão bem-sucedida ao Wi-Fi.

Define rotas e controladores de solicitações HTTP.
Inicializa uma thread separada para atualizar o LCD com a temperatura atual.
Bloco try-except para verificar se o arquivo de configuração MQTT existe.

Se existir, verifica o modo de inscrição e inicia uma thread separada para ouvir as mensagens MQTT.
Bloco final para iniciar o servidor web.
 

functions.py:

Importações:

phew, pico_temp_sensor, pico_led, json, os, utime, _thread, umail, config, usocket as socket, network, uasyncio as asyncio.
setup_mode(): função para entrar no modo de configuração do Wi-Fi.

application_mode(client): função para executar o modo de aplicação após a conexão bem-sucedida ao Wi-Fi.

Define rotas e controladores de solicitações HTTP para a aplicação.
Inicializa uma thread separada para atualizar o LCD com a temperatura atual.
Essas são as principais funcionalidades e estrutura do código fornecido. Ele lida com a leitura de temperatura, controle de LED, comunicação MQTT, configuração de Wi-Fi e servidor web para controlar um sistema de rega.
 
No arquivo main.py:

Importações: Importa os módulos e pacotes necessários para o funcionamento do código.

Inicialização de conexões: Define as conexões, como pinos de LED e configurações do LCD.
Verificação da conexão do LCD: Verifica se o LCD está conectado corretamente.
Definição das funções de controle das cores do LED: Define funções para controlar as cores do LED.
Função get_led_status(): Retorna o status atual do LED.

Função get_available_networks(): Retorna a lista de redes Wi-Fi disponíveis.

Função check_temp(): Lê a temperatura atual usando um sensor analógico.

Função read_temp(): Lê a temperatura atual e retorna uma string formatada.

Função read_temp_lcd(): Exibe a temperatura no LCD, se estiver conectado.

Função machine_reset(): Reinicia o Raspberry Pi Pico.

Configuração do MQTT: Define as configurações relacionadas ao MQTT, como tópicos, funções de callback e conexão.

Bloco try-except: Verifica se existe um arquivo de configuração do Wi-Fi e inicia o cliente MQTT.

application_mode(): Executa o modo de aplicação após a conexão bem-sucedida ao Wi-Fi. Define rotas e controladores de solicitações HTTP.

Bloco try-except para verificar se o arquivo de configuração MQTT existe. Inicia uma thread separada para ouvir as mensagens MQTT.
Bloco final para iniciar o servidor web.

No arquivo functions.py:

Importações: Importa os módulos e pacotes necessários para o funcionamento do código.
setup_mode(): Entra no modo de configuração do Wi-Fi, onde o usuário pode fornecer as informações de SSID e senha.

application_mode(client): Executa o modo de aplicação após a conexão bem-sucedida ao Wi-Fi. Define rotas e controladores de solicitações HTTP para a aplicação.


Essas são as principais partes do código e o que cada trecho faz. Cada função desempenha um papel específico no controle do sistema de rega, comunicação MQTT, atualização do LCD e configuração do Wi-Fi.


#### FLASK - Painel de controlor


## Bibliografia  

- [Peppe8o](https://peppe8o.com/mqtt-and-raspberry-pi-pico-w-start-with-mosquitto-micropython/)
- [Steve´s Internet Guide](http://www.steves-internet-guide.com/mqtt/)
- [Tomshardware](https://www.tomshardware.com/how-to/connect-raspberry-pi-pico-w-to-the-internet)
