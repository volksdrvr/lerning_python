import logging
import boto3
from datetime import date, datetime
from botocore.exceptions import ClientError
import json

AWS_REGION = 'us-west-2'

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

vpc_client = boto3.client("ec2", region_name=AWS_REGION)


def json_datetime_serializer(obj):
    """
    Helper method to serialize datetime fields
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def describe_nat_gateways(tag, tag_values, max_items):
    """
    Describes one or more of your NAT gateways.
    """
    try:
        # creating paginator object for describe_nat_gateways() method
        paginator = vpc_client.get_paginator('describe_nat_gateways')

        # creating a PageIterator from the paginator
        response_iterator = paginator.paginate(
            Filters=[{
                'Name': f"tag:{tag}",
                'Values': tag_values
            }],
            PaginationConfig={'MaxItems': max_items})

        full_result = response_iterator.build_full_result()

        nat_gateways_list = []

        for page in full_result['NatGateways']:
            nat_gateways_list.append(page)

    except ClientError:
        logger.exception('Could not describe NAT Gateways.')
        raise
    else:
        return nat_gateways_list


if __name__ == '__main__':
    print ("I am running as main")
    # Constants
    TAG = 'Name'
    TAG_VALUES = ['hands-on-cloud-nat-gateway']
    MAX_ITEMS = 10
    nat_gateways = describe_nat_gateways(TAG, TAG_VALUES, MAX_ITEMS)
    logger.info('NAT Gateways Details: ')
    for nat_gateway in nat_gateways:
        logger.info(
            json.dumps(nat_gateway, indent=4, default=json_datetime_serializer)
            + '\n')

print ('i am not running as main')
print("Value in built variable name is:  ",__name__)