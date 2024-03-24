import yaml
import etcd3

# Create an instance of Etcd3Client
client = etcd3.client()

def parse_yaml_and_store(customer_input_infra, client):
    with open(customer_input_infra, 'r') as file:
        data = yaml.safe_load(file)

    tenant_name = data['tenant_name']
    
    # Create a nested dictionary to store the data
    tenant_data = {tenant_name: {}}
    for vpc in data['vpcs']:
        vpc_name = vpc['name']
        tenant_data[tenant_name][vpc_name] = {}
        for subnet in vpc['subnets']:
            subnet_name = subnet['name']
            tenant_data[tenant_name][vpc_name][subnet_name] = {}
            for vm in subnet['VMs']:
                vm_name = vm['name']
                tenant_data[tenant_name][vpc_name][subnet_name][vm_name] = {
                    'model': vm['model'],
                    'RAM_size': vm['RAM_size'],
                    'CPUs': vm['CPUs'],
                    'disk_size': vm['disk_size']
                }
    
    # Store the nested dictionary in etcd
    client.put(tenant_name, str(tenant_data))

if __name__ == "__main__":
    # Parse YAML and store data in etcd
    parse_yaml_and_store('customer_input_infra.yaml', client)




# import yaml
# import etcd3

# # Create an instance of Etcd3Client
# client = etcd3.client()

# def parse_yaml_and_store(customer_input_infra, client):
#     with open(customer_input_infra, 'r') as file:
#         data = yaml.safe_load(file)

#     for vpc in data['vpcs']:
#         vpc_name = vpc['name']
#         for subnet in vpc['subnets']:
#             subnet_name = subnet['name']
#             for vm in subnet['VMs']:
#                 vm_name = vm['name']
#                 vm_data = {
#                     'model': vm['model'],
#                     'RAM_size': vm['RAM_size'],
#                     'CPUs': vm['CPUs'],
#                     'disk_size': vm['disk_size']
#                 }
#                 key = f"/{vpc_name}/{subnet_name}/{vm_name}"
#                 client.put(key, str(vm_data))

# if __name__ == "__main__":
#     # Parse YAML and store data in etcd
#     parse_yaml_and_store('customer_input_infra.yaml', client)




# import yaml
# import etcd3

# # Create an instance of Etcd3Client
# client = etcd3.client()

# def parse_yaml_and_store(customer_input_infra, client):
#     with open(customer_input_infra, 'r') as file:
#         data = yaml.safe_load(file)

#     # for org in data:
#     #     org_name = org['name']
#     for vpc in org['vpcs']:
#         vpc_name = vpc['name']
#         for subnet in vpc['subnets']:
#             subnet_name = subnet['name']
#             for vm in subnet['VMs']:
#                 vm_name = vm['name']
#                 vm_data = {
#                     'model': vm['model'],
#                     'RAM_size': vm['RAM_size'],
#                     'CPUs': vm['CPUs'],
#                     'disk_size': vm['disk_size']
#                 }
#                 key = f"/{org_name}/{vpc_name}/{subnet_name}/{vm_name}"
#                 client.put(key, str(vm_data))

# if __name__ == "__main__":
#     # Parse YAML and store data in etcd
#     parse_yaml_and_store('customer_input_infra.yaml', client)



# import yaml
# import etcd3

# Client = etcd3.client()

# def parse_yaml_and_store(customer_input_infra, client):
#     with open(customer_input_infra, 'r') as file:
#         data = yaml.safe_load(file)

#     for org in data:
#         org_name = org['name']
#         for vpc in org['vpcs']:
#             vpc_name = vpc['name']
#             for subnet in vpc['subnets']:
#                 subnet_name = subnet['name']
#                 for vm in subnet['VMs']:
#                     vm_name = vm['name']
#                     vm_data = {
#                         'model': vm['model'],
#                         'RAM_size': vm['RAM_size'],
#                         'CPUs': vm['CPUs'],
#                         'disk_size': vm['disk_size']
#                     }
#                     key = f"/{org_name}/{vpc_name}/{subnet_name}/{vm_name}"
#                     client.put(key, str(vm_data))

# if __name__ == "__main__":
#     # Connect to local etcd server
#     etcd_client = Client('localhost', 2379)

#     # Parse YAML and store data in etcd
#     parse_yaml_and_store('customer_input_infra.yaml', etcd_client)
