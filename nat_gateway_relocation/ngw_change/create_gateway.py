import logging
import boto3
import time
from collections import defaultdict
from datetime import date, datetime
from botocore.exceptions import ClientError
import json

AWS_REGION = 'us-west-2'

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

client = boto3.client("ec2", region_name=AWS_REGION)


def json_datetime_serializer(obj):
    """
    Helper method to serialize datetime fields
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


# def wait_nat_creation(nat_gateway_id):
#     """
#     Check if successful state is reached every 15 seconds until a successful state is reached.
#     An error is returned after 40 failed checks.
#     """
#     try:
#         waiter = client.get_waiter('nat_gateway_available')
#         waiter.wait(NatGatewayIds=[nat_gateway_id])
#     except ClientError:
#         logger.exception(f'Could not create the NAT gateway.')
#         raise

def status_ngw(nat_gateway_id):
    response = client.describe_nat_gateways(
    NatGatewayIds=[
        nat_gateway_id,
    ])
    current_ngw_status = response['NatGateways'][0]['State']
    print ('status_ngw is returning:', current_ngw_status)
    return current_ngw_status

def wait_nat_create(nat_gateway_id, wait_time):
    """
    Check if successful state is reached every 15 seconds until a successful state is reached.
    An error is returned after 40 failed checks.
    """
    start_time = time.time()
    seconds = wait_time

    while True:
        time.sleep(10)
        current_time = time.time()
        elapsed_time = current_time - start_time
        status_returned = status_ngw(nat_gateway_id)
        
        if status_returned == 'available':
            print (status_returned)
            break
        elif elapsed_time > seconds:
            print('The desired wait_time has been exceeded:', str(int(elapsed_time)), 'seconds')
            print ('The last status returned was:', status_returned)
            break
        else:
            print ('The curent status is:', status_returned)
    return status_returned

def create_ngw(orig_subnet_id, allocation_id, tags, wait_time):
    """
    Creates a NAT gateway in the specified subnet.
    """
    try:
        
        response = client.create_nat_gateway(
            AllocationId=allocation_id,
            SubnetId=orig_subnet_id,
            TagSpecifications=[
                {
                    'ResourceType': 'natgateway',
                    'Tags': tags
                },
            ],
            ConnectivityType='public'
        )
        
            
        nat_gateway_id = response['NatGateway']['NatGatewayId']
 
        status_returned = wait_nat_create(nat_gateway_id, wait_time)
        print ('I am in create_ngw', status_returned)
        print (response)


        
        return response

    except ClientError:
        logger.exception(f'Could not create the NAT gateway.')
        raise
    else:
        return response

# if __name__ == '__main__':
