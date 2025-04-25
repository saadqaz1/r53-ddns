# py-aws-r53-dns

## Overview

Python script used as CRON job to check WAN IP and update a AWS Route 53 DNS record accordingly.

## Usage
1. Clone repo into local working directory

    `git clone https://github.com/saadqaz1/py-aws-r53-dns.git`

2. Create `.env` file for
    - AWS keys
    - R53 domain name and zone id
    - log path

    >sudo nano .env

    ```
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    DOMAIN=''
    ZID=''
    LOG_PATH='/home/pi/pyawsdns'
    ```
3. Create a virtual env

    `python3 -m venv env`

    `source env/bin/activate`

4. Install req.txt

    `pip install -r req.txt`

3. Run `python3 awsdns.py`

## Schedule

1. Modify crontab to run job every X time (in this case every 30 minutes)

    `crontab -e`

    Example CRON:
    ```
    # m h  dom mon dow   command
    SHELL=/bin/bash
    */30 * * * * /usr/bin/python3 /home/pi/pyawsdns/awsdns.py
    ```
