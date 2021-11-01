import logging
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
# tables. https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-nat-gateway.html

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

client = boto3.client('ec2')

def status_eip(eip_allocation_id):
    """
    Deletes the specified NAT gateway.
    """
    print('hi from eip status:',  eip_allocation_id)
    response = client.describe_addresses(
        AllocationIds=[
            eip_allocation_id,
        ]
    )

    print (response)

    
    # try:
    #     response = vpc_client.delete_nat_gateway(NatGatewayId=nat_gateway_id)

    # except ClientError:
    #     logger.exception('Could not delete the NAT Gateway.')
    #     raise
    # else:
    #     return response


# if __name__ == '__main__':
