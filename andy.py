# #import describe_nat_gateway
# import create_nat_gateway

# #52.xxx.xxx.xxx my route53 entry for blog
# #myvar = describe_nat_gateway.describe_nat_gateways(tag, tag_values, max_items)


# #current_subnet = 'subnet-0f6cb2238d29ec05e'
# #create_nat_gateway.create_nat(current_subnet)

# # Use the job to set the key name for each resource. Create a dictionary 
# # for each resource listing the AWS "Name" of each affected natgateway

# RESOURCE_ENV=

# resource_dict = {
#     'resource_env1': ('k8s-env', 'k8s-env'),
#     'resource_env2': ('k8s-env', 'k8s-env')
#     }

# Defined
def return_ngw_atributes(nats_to_return):
    ngw_instances = defaultdict(ngw.describe_gateway.describe_ngw(nats_to_return))
    
    #print (ngw_instances)
    for tag in ngw_instances['Tags']:
        #print (tag)
        if 'Name' in tag['Key']:
            tag_name = tag['Value']
            #print(tag_name)
            break
    
    ngw_attributes[tag_name] = {
        'NetworkInterfaceId': ngw_instances['NatGatewayAddresses'][0]['NetworkInterfaceId'],
        'ConnectivityType': ngw_instances['ConnectivityType'],
        'NatGatewayId': ngw_instances['NatGatewayId'],
        'AllocationId': ngw_instances['NatGatewayAddresses'][0]['AllocationId'],
        'PrivateIp': ngw_instances['NatGatewayAddresses'][0]['PrivateIp'],
        'PublicIp': ngw_instances['NatGatewayAddresses'][0]['PublicIp'],
        'SubnetId': ngw_instances['SubnetId'],
        'State': ngw_instances['State'],
        'Tags': ngw_instances['Tags'], 
    }
    return ngw_instances