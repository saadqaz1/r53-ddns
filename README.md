# py-aws-r53-dns
Python script used as CRON job to check WAN IP of raspberry pi and update AWS Route 53 record accordingly.

create and clone rep into local dir

`mkdir pyawsdns && cd pyawsdns`

`git clone https://github.com/knightfall23/py-aws-r53-dns.git`

create and add .env vars files in dir for domain name, zone id and log path (may need to create blank logfile)

>sudo nano .env


```
DOMAIN=''
ZID=''
LOG_PATH='/home/pi/pyawsdns'
```

next modify crontab to run job every X time (in this case every 30 minutes)

`crontab -e`
```
# m h  dom mon dow   command
SHELL=/bin/bash
*/30 * * * * /usr/bin/python3 /home/pi/pyawsdns/awsdns.py
```

