from collections import defaultdict
import ngw_change as ngw
import boto3


# used for testing until it runs


#################################################################################
# The name of the natgateway is stored as a constant defined with the name of the
# service(s) affected. Use the job to set the variable targeted_nats for the key
# of RESOURCE_ENV which is a dictionary of string arrays each AWS resource tag
# name of each affected nat gateway.

targeted_aws_region = 'us-west-2'
targeted_nats = "k8s-prod"
time_to_wait = 600

RESOURCE_ENV = {
    "k8s-non-prod": ['k8s-env-delete-me1'],
    "k8s-prod": ['k8s-env-delete-me0', 'k8s-env-delete-me1']
}


#################################################################################
# Make note of the associated with the NAT Gateway
# Obtain all of the needed argumnets to delete\create a natgateway while
# maintaining the current attributes using the same EIP and to increment the
# avalability zone by 1.
# name - RESOURCE_ENV
# -subnet
# -connectivity type
# -elastic ip allocation id
# -tags

ngw_instances = ngw.describe_gateway.describe_ngw(RESOURCE_ENV[targeted_nats])

ngw_orig_attributes = defaultdict()
# print('Iam the ngw_instances output:', ngw_instances)
# print('Ijust want the tags:', ngw_instances[0]['Tags'])
# print('Ijust want the NatGatewayId:', ngw_instances[0]['NatGatewayId'])

# ec2 = boto3.resource('ec2')
# ngw = ec2.NATGateway(ngw_instances[0]['NatGatewayId'])
# tag = ngw.Tag(ngw_instances[0]['NatGatewayId'],'IwantA','sexyKey')

# print(tag)


for instance in ngw_instances:
    #print (instance)
    for tag in instance['Tags']:
        #print (tag)
        if 'Name' == tag['Key']:
            tag_name = tag['Value']
            #print(tag_name)
            break
   
    ngw_orig_attributes[tag_name] = {
        'NetworkInterfaceId': instance['NatGatewayAddresses'][0]['NetworkInterfaceId'],
        'ConnectivityType': instance['ConnectivityType'],
        'NatGatewayId': instance['NatGatewayId'],
        'AllocationId': instance['NatGatewayAddresses'][0]['AllocationId'],
        'PrivateIp': instance['NatGatewayAddresses'][0]['PrivateIp'],
        'PublicIp': instance['NatGatewayAddresses'][0]['PublicIp'],
        'SubnetId': instance['SubnetId'],
        'State': instance['State'],
        'Tags': instance['Tags'], 
    }

print ('\nThe following resources will be deleted and re-created:')
for foo, bar in ngw_orig_attributes.items():
    print (foo)
    for fubar, barfoo in bar.items():
        print ("{}: {}".format(fubar, barfoo))
    print ('\n')

#################################################################################
# Delete the NAT Gateway(s)
for foo, bar in ngw_orig_attributes.items():
    print ('This is the ngw name to be delete:',foo,'in', targeted_aws_region)
    print ('This is the ngw id to be delete',bar['NatGatewayId'])
    nat_gateway_delete = ngw.delete_gateway.delete_ngw(bar['NatGatewayId'], time_to_wait)

#################################################################################
# Wait for the eip to be released...

# eip does not have a status return

# for foo, bar in ngw_orig_attributes.items():
#     print ('We are waiting on the status of this eip:', foo, 'in', targeted_aws_region)
#     print ('This is the allocation id of the eip',bar['AllocationId'])
#     eip_status = ngw.eip_status.status_eip(str(bar['AllocationId']))
#     print (eip_status)
# time.sleep(10)
#################################################################################
# Create new NAT Gateway with the same elastic ip address found in step 1

# nat_gateway_create = ngw.create_gateway.create_ngw(
#         'subnet-0f6cb2238d29ec05e',
#         'eipalloc-0654f7a61a005c9a3',
#         time_to_wait
#         )

for foo, bar in ngw_orig_attributes.items():
    nat_gateway_create = ngw.create_gateway.create_ngw(
        bar['SubnetId'],
        bar['AllocationId'],
        bar['Tags'],
        time_to_wait
        )
    
ngw_new_attributes = defaultdict()

for instance in ngw_instances:
    #print (instance)
    for tag in instance['Tags']:
        #print (tag)
        if 'Name' in tag['Key']:
            tag_name = tag['Value']
            #print(tag_name)
            break
   
    ngw_new_attributes[tag_name] = {
        'NetworkInterfaceId': instance['NatGatewayAddresses'][0]['NetworkInterfaceId'],
        'ConnectivityType': instance['ConnectivityType'],
        'NatGatewayId': instance['NatGatewayId'],
        'AllocationId': instance['NatGatewayAddresses'][0]['AllocationId'],
        'PrivateIp': instance['NatGatewayAddresses'][0]['PrivateIp'],
        'PublicIp': instance['NatGatewayAddresses'][0]['PublicIp'],
        'SubnetId': instance['SubnetId'],
        'State': instance['State'],
        'Tags': instance['Tags'], 
    }

print ('\nThe following resources will be deleted and re-created:')
for foo, bar in ngw_orig_attributes.items():
    print (foo)
    for fubar, barfoo in bar.items():
        print ("{}: {}".format(fubar, barfoo))
    print ('\n')

#################################################################################
# Update Route Tables associated with the  private subnets in the VPC to to use the new NAT Gateway
