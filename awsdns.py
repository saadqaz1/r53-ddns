import os, boto3, logging
import requests
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
        WIP = get('https://checkip.amazonaws.com')
        print("Current Public IP: " + WIP.text.strip())
    except requests.exceptions.RequestException as e:
        print(e)
    return WIP


def checkIfIPChanged():
    response = client.list_resource_record_sets(
    HostedZoneId=ZID,
    StartRecordName=DOMAIN,
    StartRecordType='A',
    MaxItems='1'
    )
    DOMAINIP = response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
    WANIP = getPublicIp()
    if WANIP.text.strip() == DOMAINIP.strip():
        print('SAME IP...')
        return False
    elif WANIP != DOMAINIP:
        print('DIFF IP...')
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
        logger('Change Detected...Updating IP...')
    else:
        logger('There was no change to IPs...Exiting...')
        return
main()
