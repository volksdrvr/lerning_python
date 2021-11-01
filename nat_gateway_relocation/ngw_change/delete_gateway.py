import logging
from os import stat
import time
import boto3
from botocore.exceptions import ClientError
import json

current_session = boto3.session.Session()
AWS_REGION = current_session.region_name

#################################################################################
# Notes from AWS:
# Deletes the specified NAT gateway. Deleting a public NAT gateway disassociates 
# its Elastic IP address, but does not release the address from your account. 
# Deleting a NAT gateway does not delete any NAT gateway routes in your route 
# tables. 
# https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-nat-gateway.html

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

client = boto3.client("ec2", AWS_REGION)

def status_ngw(nat_gateway_id):
    response = client.describe_nat_gateways(
    NatGatewayIds=[
        nat_gateway_id,
    ])
    current_ngw_status = response['NatGateways'][0]['State']
    print ('status_ngw is returning:', current_ngw_status)
    return current_ngw_status

def wait_nat_delete(nat_gateway_id, wait_time):
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
        
        if status_returned == 'deleted':
            print (status_returned)
            break
        elif elapsed_time > seconds:
            print('The desired wait_time has been exceeded:', str(int(elapsed_time)), 'seconds')
            print ('The last status returned was:', status_returned)
            break
        else:
            print ('The curent status is:', status_returned)
    return status_returned
    # try:

    # except ClientError:
    #     logger.exception(f'Could not create the NAT gateway.')
    #     raise

def delete_ngw(nat_gateway_id, wait_time):
    """
    Deletes the specified NAT gateway.
    """
        
    try:
        response = client.delete_nat_gateway(NatGatewayId=str(nat_gateway_id))
        status_returned = wait_nat_delete(nat_gateway_id, wait_time)
        print ('I am in delete_ngw', status_returned)
        return status_returned

    except ClientError:
        logger.exception('Could not delete the NAT Gateway.')
        raise
    else:
        return response


# if __name__ == '__main__':
