import boto3
ec2_client = boto3.client('ec2')
waiter = ec2_client.get_waiter('nat_gateway_available')



