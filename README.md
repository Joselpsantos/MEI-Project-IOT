 
# Projeto IOT
Criação de um sistema de rega, acente na placa de desenvolvimento Raspberry Pico W (doravante denoinado de "RPW"), onde foi implementado Captive Portal para efetuar a ligação do RPW à rede WI-FI, e posterior configuração do broker num servidor WEB instalado na propria memória.
Foi desenvolvido também, em Flask, um portal de gestão utilizando Websockets.

A ligação feita pelo exterior, fica a carga da solução NGROK.



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

![image](https://github.com/Joselpsantos/MEI-Project-IOT/assets/113514374/8309ed91-469c-4f2d-b784-d2de5ef779ae)

## Recursos utilizado  

**Software:** 
- microPhyton
- VirtualBox/Vagrant
- Broker Mosquitto MQTT
- VSCODE
- Thonny  

**Hardware:** 
- 1x Raspberry Pico W (doravante denominado de RPW)
- 2x LED
- 1x LCD duas linhas 
- 5x resistências
- 14x fios de ligação

<img src="/Imagens/rpicogpin.png" width="600">
<img src="/Imagens/rpicow.jpg" width="600">


## Características  

VM´s:
- Instalação e configuração automática da VM   
- Instalação e configuração do broker Mosquitto  
- Instalação e configuração do flask com WebSockets ("WS") 

Raspberry Pico w:
- Ligar ao wireless com captive portal
- Ligação ao broker feita em página dedicada
- Envio da temperatura para o Broker
- Receção de instrução para Ligar/desligar a Rega, ou colocação em modo automático, definindo a partir de que temperatura deverá ligar o sistema.

## Iniciar o projeto 

Clonar o projeto  

~~~bash  
  git clone https://github.com/Joselpsantos/MEI-Project-IOT.git
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
Todos estes requsitos foram cumpridos, onde se utilizou o recurso Captive Portal, um painel de gestão próprio no RPW, onde se pode efetuar a ligação ao broker, e definir o tempor de rega.
Outro portal, centralizado, onde poderemos comunicar com o RPW, e podermos expandir o sistema a outros dispositivos IOT. Este portal utiliza websockets e FLASk.


Para desenvolver o programa em Python (Microphtyon), que vai ser executado no RPW, recorremos ao software <b>Thonny</b>.


## Descrição do programa desenvolvido.

Código Python que consiste em dois ficheiros principais: main.py e functions.py. 

Iremos descrever cada um deles em detalhe:

#### main.py - ficheiro responsável pela execução do código de inicialização:

<i>Importações:</i>

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
<br><br>
#### Inicialização de conexões:

<b>onboard_led, led_r, led_g, led_b</b>: pinos de LED utilizados.

<b>led_status, lcd_connected</b>: variáveis de estado para o LED e o LCD.

<b>temperature, sensor_temp, conversion_factor</b>: variáveis relacionadas à leitura de temperatura usando o sensor interno

<b>I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS</b>: constantes para configurar o LCD.

<b>Verificação da conexão do LCD</b>: Tenta inicializar o objeto lcd do tipo I2cLcd para se comunicar com o LCD.
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
<br>

<b>topic_sub, topic</b>: tópicos MQTT para assinatura e controle.

<b>sub_cb()</b>: função de callback para tratar mensagens MQTT recebidas.

<b>mqtt_connect()</b>: realiza a conexão com o servidor MQTT e retorna o objeto MQTTClient.

<b>reconnect()</b>: função para reconectar ao servidor MQTT em caso de falha na conexão.

<b>rega_on(), rega_off()</b>: funções para ligar e desligar a rega.

<b>rega_auto()</b>: função para executar o modo de rega automática com base na temperatura.

<b>update_conf_file()</b>: atualiza o ficheiro de configuração MQTT.

<b>mqtt_listener()</b>: função assíncrona para ouvir as mensagens MQTT.

<b>Função get_available_networks()</b>: Retorna a lista de redes Wi-Fi disponíveis.

<b>Função check_temp()</b>: Lê a temperatura atual usando um sensor analógico.

<b>Função read_temp()</b>: Lê a temperatura atual e retorna uma string formatada.

<b>Função read_temp_lcd()</b>: Exibe a temperatura no LCD, se estiver conectado.

<b>Função machine_reset()</b>: Reinicia o Raspberry Pi Pico.

<b>Configuração do MQTT</b>: Define as configurações relacionadas ao MQTT, como tópicos, funções de callback e conexão.

<b>Bloco try-except</b>: Verifica se existe um ficheiro de configuração do Wi-Fi e inicia o cliente MQTT.

<b>application_mode()</b>: Executa o modo de aplicação após a conexão bem-sucedida ao Wi-Fi. Define rotas e controladores de solicitações HTTP.

<b>Bloco try-except</b> para verificar se o ficheiro de configuração MQTT existe. Inicia uma thread separada para ouvir as mensagens MQTT.
Bloco final para iniciar o servidor web.

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


Define rotas e controladores de solicitações HTTP.
Inicializa uma thread separada para atualizar o LCD com a temperatura atual.
Bloco try-except para verificar se o ficheiro de configuração MQTT existe.

Se existir, verifica o modo de inscrição e inicia uma thread separada para ouvir as mensagens MQTT.
Bloco final para iniciar o servidor web.
 

Essas são as principais funcionalidades e estrutura do código presente no main.py. Ele lida com a leitura de temperatura, controle de LED, comunicação MQTT, configuração de Wi-Fi e servidor web para controlar o sistema de rega.
 

#### functions.py:

Todas as funções invocadas no main.py, estão definidas no functions.py

```
def get_available_networks():
    wlan = network.WLAN(network.STA_IF)
    networks = wlan.scan()
    return [net[0].decode() for net in networks]
```
Esta função procura pelas redes WI-FI, e retornas as mesmas para ser utilizado na página WEB.

```
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
```

Aqui estamos a definir os procedimentos que o RPW terá, quando subscrever um tópico e recebe as mensagens.

```
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
```
Na função aqui transcrita, que foi a função mais desafiante de elaborar do projeto, tem de ter em consideração uma série de cenários.
Esta função terá de estar sempre à escuta, o que implica utilização de recursos, e executar comandos, também com alguma complexidade, o que em termos de hardware acaba por ser limitado para a execução do mesmo.
Nesta função, acendemos a luz indicadora de rega em modo AUTO, vai pesquisar no ficheiro de configuração os dados do MQTT, faz o print para o LCD, obtém a temperatura atual e a definida como TARGET, e executa o comando para ligar a rega. 


#### FLASK - Painel de controlor


## Funcionamento

#### Funções assíncronas
<img src="https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Dyr7amckevWGqes1PTv0SQ.png" width="400">

Funções que executam operações demoradas (I/O ou CPU intensive), em simultâneo. O normal no código python é ser executado por ordem que aparece no código, e caso alguma linha dê erro, todo o programa crasha e pára a execução.
Com as funções assíncronas, podemos executar várias tarefas em simultâneo, e com tratamento individualizado dos erros para cada tarefa.

#### Threads
NOTA: COLOCAR IMAGEM

## Testes
Toda a solução passou por diversos testes para assegurar a correta operacionalidade.

O captive portal, foi testado em IOS, ANDROID e WINDOWS, tendo efetuado a ligação sem problemas em nenhuma das plataformas.
A conexão

## Dificuldades
Uma vez que para este projeto foi utilizado o Raspberry Pico W, que é um hardware excelente custo vs benefícios, contudo, para projetos mais elaborados, as suas caracteristicas/recursos ficam limitados.

Na execução deste projeto, utilizámos um LCD, uma ligação AP, e um broker, o que se revelou claramente exigente para o hardware.
Para contornar o problema constante de esgotar os recursos, tivemos de procurar soluções alternativas, pelo que fizemos uso de threads, e de funções assíncronas.

Mesmo utilizando estas tecnologias, reparámos que o LCD é o grande responsável por esgotar os recursos do RPW. 
Outra dificuldade, que após muitos testes, ficámos sem ter a certeza de onde estaria o problema, é que a conexão ao broker é instável. Por vezes tem dificuldade em ligar-se, e outras vezes, deixa de enviar as mensagens. Recorrendo aos logs, parece não chegar a informação por parte do RPW, contudo, o código continua a ser executado corretamente. Levanos a crer, que seja alguma instabilidade do WI-FI.

## Melhorias ao projeto
Apesar do programa estar bastante funcional, e cheio de recursos, consideramos que há lugar para melhorarias ao sistema.

Passamos a elencar as mesmas:
- optimizar o código;
- adicionar um LED específico para o modo AUTO;
- melhorar em termos gráficos a administração, tanto em termos de RPW como de FLASK;
- implementar uma solução melhor de conectividade exterior
- 
- 


## Conclusão
No final este projeto, ficámos capazes de programar um dispositivo IOT, denominado de RaspBerry Pico W, configurar um Broker MQTT, e gerir as ligações ao mesmo, protocolos de segurança como o "SSH, reverse tunnel, ngrok - explorar estes mecanismos"

## Bibliografia  

- [Peppe8o](https://peppe8o.com/mqtt-and-raspberry-pi-pico-w-start-with-mosquitto-micropython/)
- [Steve´s Internet Guide](http://www.steves-internet-guide.com/mqtt/)
- [Tomshardware](https://www.tomshardware.com/how-to/connect-raspberry-pi-pico-w-to-the-internet)
