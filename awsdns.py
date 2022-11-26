 #aws dns boto r53 qpitor update
import os, boto3, logging
import requests
import sys, subprocess
from datetime import datetime 
from requests import get
from dotenv import load_dotenv

load_dotenv()

ZID = os.getenv('ZID')
DOMAIN = os.getenv('DOMAIN')
LOG_PATH = os.getenv('LOG_PATH')

client = boto3.client('route53') 

def logger(message):
    dt = datetime.now() 
    print (message)
    logging.basicConfig(filename=LOG_PATH+'/pyawsdns.log', level=logging.INFO) 
    logging.info(dt.isoformat() +': '+ message)

def getPublicIp():
    try:
        WIP = get('https://ifconfig.me')
        os.environ["HOME_IP"] = WIP.text
        print('ifconfig status code: ' + WIP.status_code)
    except requests.exceptions.RequestException as e:
        logger(e)
        print(e)
    return WIP.text

def runAnsibleSg():
    try:
        HOME_IP=os.environ["HOME_IP"]+"/32"
        print(HOME_IP)
        cmd = ["ansible-playbook", "-e",  f"HOME_IP={HOME_IP}", "update_sg.yml" ]
        print(cmd)
        subout = subprocess.run(cmd, capture_output=True)
        logger(subout.stdout.decode())
    except requests.exceptions.RequestException as e:
        print(e)
        logger(e)

def checkIfIPChanged():
    R53Response = client.list_resource_record_sets(
    HostedZoneId=ZID,
    StartRecordName=DOMAIN,
    StartRecordType='A',
    MaxItems='1'
    )
    print('R53Response: ' + R53Response)
    logger('R53Response: ' + R53Response)
    DOMAINIP = R53Response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
    WANIP = getPublicIp()
    if WANIP == DOMAINIP:
        logger('SAME IP...' + DOMAINIP)
        return False
    elif WANIP != DOMAINIP:
        logger('DIFFERENT IP...' + WANIP)
        return True

def updateRecordIP(WANIP):
    response = client.change_resource_record_sets(
    HostedZoneId=ZID,
    ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': DOMAIN,
                        'Type': 'A',
                        'TTL': 180,
                        'ResourceRecords': [
                            {
                                'Value': WANIP
                            },
                        ]
                    }
                },
            ]
        }
    )
    #print r53 change response
    print(response)
    CID = response['ChangeInfo']['Id']
    logger(CID)

def main():
    logger('***pyawsdns starting***')
    if checkIfIPChanged() == True:
        WIP = getPublicIp()
        updateRecordIP(WIP)
        logging.info(dt.isoformat() +': NEW WIP IS: '+ WIP)
        logger('Change Detected...Updating R53 IP...')
        logger('Change Detected...Updating SG IP Baselines...')
        runAnsibleSg()
    else:
        logger('There was no change to IP\'s...Exiting...')
        return
main()
