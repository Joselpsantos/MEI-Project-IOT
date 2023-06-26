#!/bin/bash

# Atualizar os pacotes
sudo apt-get update

# Instalar o pacote net-tools
sudo apt install net-tools

# Instalar o Mosquitto MQTT
sudo apt-get install -y mosquitto mosquitto-clients

# Definir a password
sudo mosquitto_passwd -c /etc/mosquitto/credentials pico <<<$'pico\npico'

# Copiar o ficheiro de configuração do mosquitto
cp ../../vagrant/provision/mosquitto.conf /etc/mosquitto/mosquitto.conf
echo "Copiado ficheiro da configuração MOSQUITTO com sucesso."

# Iniciar o Mosquitto MQTT
sudo systemctl restart mosquitto.service

# Mostra o IP da máquina
echo 'IP da máquina virtual mqtt-broker:' && hostname -I | awk '{print $2}'