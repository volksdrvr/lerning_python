import logging
import boto3
from datetime import date, datetime
from botocore.exceptions import ClientError
import json

current_session = boto3.session.Session()
AWS_REGION = current_session.region_name

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

vpc_client = boto3.client("ec2", AWS_REGION )


def json_datetime_serializer(obj):
    """
    Helper method to serialize datetime fields
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def describe_ngw(list_ngw_passed):
    """
    Describes one or more of your NAT gateways.
    """
    max_items = 1000
    
    try:
        # creating paginator object for describe_ngw() method
        paginator = vpc_client.get_paginator('describe_nat_gateways')

        # creating a PageIterator from the paginator
        response_iterator = paginator.paginate(
            Filters=[
                {
                    'Name': f"tag:Name",
                    'Values': list_ngw_passed
                },
                {
                    'Name': f"tag:Name",
                    'Values': ['k8s-env-delete-me1']
                }
                
                ],
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


# if __name__ == '__main__':
