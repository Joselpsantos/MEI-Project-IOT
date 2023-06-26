MSG_COLOR="\033[41m"
#Install Python

#sudo apt install npm
echo -e "$MSG_COLOR$(hostname): Python Instalation\033[0m"
sudo apt-get install python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-virtualenv -y

echo -e "$MSG_COLOR$(hostname): Create virtual environment\033[0m"
sudo apt install python3-venv -y

echo -e "$MSG_COLOR$(hostname): Create flask and change to this directory\033[0m"
sudo mkdir /home/flask
sudo mkdir /home/webpage && cd /home/webpage
sudo mkdir /home/webpage/templates

cd 

echo -e "$MSG_COLOR$(hostname): Copy the app file to the flask directory\033[0m"
cp ../../vagrant/WebPage/app.py /home/webpage/app.py

echo -e "$MSG_COLOR$(hostname): Copy the template file to the flask directory\033[0m"
cp ../../vagrant/WebPage/templates/index.html /home/webpage/templates/index.html
cp ../../vagrant/WebPage/templates/config-mqtt.html /home/webpage/templates/config-mqtt.html

echo -e "$MSG_COLOR$(hostname): Create flask virtual environment\033[0m"
cd
virtualenv flask

echo -e "$MSG_COLOR$(hostname): Activate flask virtual environment\033[0m"
source flask/bin/activate

echo -e "$MSG_COLOR$(hostname): Install flask and dependencies\033[0m"
pip install flask Flask-MQTT Flask-SocketIO eventlet Flask-Bootstrap gevent netifaces
pip install eventlet


#MSG_COLOR="\033[41m"
#Install Python

#sudo apt install npm
#echo -e "$MSG_COLOR$(hostname): Python Instalation\033[0m"
#sudo apt-get install python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-virtualenv -y

#echo -e "$MSG_COLOR$(hostname): Create virtual environment\033[0m"
#sudo apt install python3-venv -y

#echo -e "$MSG_COLOR$(hostname): Create flask and change to this directory\033[0m"
#sudo mkdir /home/flask && cd /home/flask
#sudo mkdir templates

#echo -e "$MSG_COLOR$(hostname): Create flask virtual environment\033[0m"
#virtualenv flask

#echo -e "$MSG_COLOR$(hostname): Activate flask virtual environment\033[0m"
#source flask/bin/activate

#echo -e "$MSG_COLOR$(hostname): Install flask and dependencies\033[0m"
#pip install flask Flask-MQTT Flask-SocketIO eventlet Flask-Bootstrap gunicorn gevent

#echo -e "$MSG_COLOR$(hostname): Copy the app file to the flask directory\033[0m"
#cp ./WebPage/app.py /home/flask/

#echo -e "$MSG_COLOR$(hostname): Copy the template file to the flask directory\033[0m"
#cp ./WebPage/templates/index.html /home/flask/templates
#cp ./WebPage/templates/config-mqtt.html /home/flask/templates
#aplicar o gunicorn como variável de path
#export PATH="/home/vagrant/.local/bin:$PATH"

#mosquitto_sub -d -P pico --username pico -t jose
#gunicorn -b 192.168.45.10:5000 --workers 4 --threads 100 app:app --timeout 200
#pip install gevent

# 1 iniciar ambiente virtual
#2 ir para diretoria flask
#3 python app.py
# LUMEEE