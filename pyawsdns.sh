#!/bin/bash
echo 'starting pyawsdns script'
source /etc/opt/py-aws-r53-dns/env-py/bin/activate
python3 /etc/opt/py-aws-r53-dns/awsdns.py
