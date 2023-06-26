sudo apt install openssh-server

mkdir duckdns

cd duckdns

echo "echo url="https://www.duckdns.org/update?domains=exampledomain&token=a7c4d0ad-114e-40ef-ba1d-d217904a50f2&ip=" | curl -k -o ~/duckdns/duck.log -K -" > duck.sh

#tornar o ficheiro executável
chmod 700 duck.sh

#criar cronjob
crontab -e

*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1

./duck.sh

cat duck.log