# 🛰️ r53-ddns Overview
r53-ddns is a Python script designed to function as a basic Dynamic DNS (DDNS) client. It checks your public WAN IP and updates an AWS Route 53 CNAME record accordingly. Ideal for dynamic IP environments where static DNS records are not feasible.

This script is typically scheduled via cron and works well on systems like Raspberry Pi or small VPS servers.

## Features
- Detects changes to your public IP address

- Automatically updates AWS Route 53 DNS CNAME records

- Logs actions to a specified file

- Easy to deploy and configure

## 🚀 Usage Instructions

1. Clone the repo
    ```bash
    git clone https://github.com/saadqaz1/r53-ddns.git
    cd r53-ddns
    ```

2. Configure Environment Variables
    Create a `.env` file in the root directory with the following structure:
    ```.env
    AWS_ACCESS_KEY_ID=your_aws_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret
    DOMAIN='your.domain.com'
    ZID='your_hosted_zone_id'
    LOG_PATH='/home/pi/pyawsdns'
    ```
    To edit:
    ```bash
    nano .env
    ```
3. Set Up Python Environment
    ```
    python3 -m venv env
    source env/bin/activate
    pip install -r req.txt
    ```

4. Run the script
    ```
    python3 awsdns.py
    ```

## ⏲️ Set Up as a Cron Job
To run the script every 30 minutes:

```
crontab -e
```

Add the following entry:
```
# m h  dom mon dow   command
SHELL=/bin/bash
*/30 * * * * /usr/bin/python3 /home/pi/pyawsdns/awsdns.py
```
Make sure the path matches your script location and Python interpreter.

*TODO: Update with shell script usage

## 📝 Notes
Requires AWS IAM credentials with permissions to manage Route 53 records.

This script assumes you are updating a CNAME record. Modify it accordingly for A or other record types if needed.

Logs are saved to the specified LOG_PATH directory.
