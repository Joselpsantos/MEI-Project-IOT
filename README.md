 
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
- 1x Raspberry Pico
- 1x Relay 2 canais
- 2x LED
- 1x LCD duas linhas 


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
Este comando é útil se você deseja economizar espaço em disco.
#### Aviso: este comando destruirá os bancos de dados do seu site.
Backup da BD: sql-dump > db.sql 
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

Escrever relatório

## Bibliografia  

- [Peppe8o](https://peppe8o.com/mqtt-and-raspberry-pi-pico-w-start-with-mosquitto-micropython/)
- [Steve´s Internet Guide](http://www.steves-internet-guide.com/mqtt/)
- [Tomshardware](https://www.tomshardware.com/how-to/connect-raspberry-pi-pico-w-to-the-internet)
