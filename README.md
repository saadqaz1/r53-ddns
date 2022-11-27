# py-aws-r53-dns
This is a Python script used as a ad-hoc DDNS via CRON jobs to check the WAN IP of the host and update an AWS route53 record and vpc security group ip accordingly.

1. create and clone this repo into your local dir or ~/opt/

`git clone https://github.com/knightfall23/py-aws-r53-dns.git`

2. cd into /py-aws-r53-dns

`cd pyawsdns`

3. create and add .env vars files in dir for domain name, zone id, log path and aws creds (may need to create blank logfile)

`sudo nano .env`

```
AWS_ACCESS_KEY_ID='<YOUR-KEY-HERE>'
AWS_SECRET_ACCESS_KEY='<YOUR-KEY-HERE>'
DOMAIN='<YOUR-R53-DOMAIN>'
ZID='<YOUR-R53-ZONE-ID>'
LOG_PATH='/opt/py-aws-r53-dns'
```

4.To test run the script by creating a python virtual enviroment and activate it in the working dir

`python3 -m venv env`

`source env/bin/activate`

5. install pip dependencies

```
pip3 install boto3
pip3 install requests
pip3 install dotenv
pip3 install wheel
pip3 install python-dotenv
pip3 install ansible
```
or pip install -r req.txt
``

6. create ansible-secrets.yml file for ansible 

```
AWS_ACCESS_KEY_ID: <YOUR-KEY-HERE>
AWS_SECRET_ACCESS_KEY: <YOUR-KEY-HERE>
DEFAULT_REGION: <YOUR-REGION-HERE>
VPC_ID: <YOUR-ID-HERE>
SECURITY_GROUP: <YOUR-SG-HERE>
```
7. run ansible-playbook 

`ansible-playbook -e @ansible-secrets.yml update_sg.yml --extra-vars "HOME_IP=9.9.9.9/32"`

6. next modify crontab to run shell script every x amount of times(in this case every 30 minutes)

`crontab -e`

```
# m h  dom mon dow   command
SHELL=/bin/bash
*/30 * * * * /etc/opt/py-aws-r53-dns/pyawsdns.sh
```


### TODOS
- dockerize script
- add retries for wip check
- 