import logging
import boto3
import time
from collections import defaultdict
from datetime import date, datetime
from botocore.exceptions import ClientError
import json

AWS_REGION = 'us-west-2'
tags = [{'Key': 'ExtraTagName', 'Value': 'ExtraTagValue'}, {'Key': 'Name', 'Value': 'k8s-env-delete-me1'}]
tag_specification = [{'ResourceType': 'ec2', 'Tags': tags},]

client = boto3.client("ec2", region_name='us-west-2')

response = client.describe_route_tables(
    Filters=[
        {
            'Name': 'route.nat-gateway-id',
            'Values': [
                'nat-xxx',
            ]
        },
    ]
)
# response = client.create_nat_gateway(
#     AllocationId='eipalloc-0654f7a61a005c9a3',
#     SubnetId='subnet-0f6cb2238d29ec05e',
#     TagSpecifications=[
#         {
#             'ResourceType': 'natgateway',
#             'Tags': tags
#         },
#     ],
#     ConnectivityType='public'
# )

response = client.describe_nat_gateways(
    Filters=[
        {
            'Name': 'state',
            'Values': [
                'available',
            ]
        },
        {
            'Name': f"tag:Name",
            'Values': [
                'k8s-env-delete-me1',
            ]
        }
    ]
)

print(response)