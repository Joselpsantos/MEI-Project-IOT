
#Install npm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

source ~/.bashrc

nvm install --lts

npm install -g localtunnel

lt --subdomain meiiotipt --port 5000