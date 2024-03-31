import etcd3
import subprocess
from ansible_runner import run
import yaml

client = etcd3.client()

# Function to run Ansible playbook
def run_playbook(filename): #, vars_dict):
    config = {
        'private_data_dir': './',
        'playbook': filename,
        # 'extravars': vars_dict
    }
    result = run(**config)
    return

def create_resources(tenant_data):
    # Implement your logic to create resources using Ansible playbook
    # You can call an Ansible playbook using subprocess module
    # After the resources are created, update the state to 'active'
    # Example: subprocess.run(['ansible-playbook', 'your_playbook.yml'])
    run_playbook('deploy.yaml') #, {'vpc_name': vpc['name']})
    return

def check_and_update_state(tenant_name, tenant_data):
    # Check the state of VPCs, subnets, and VMs
    # If any resource is in 'requested' state, call create_resources
    # and update the state to 'active'
    # Example:
    for vpc in tenant_data[tenant_name]['vpcs']:
        if vpc['state'] == 'requested':
            create_resources(tenant_data)
            vpc['state'] = 'active'
            # Update the state in the database
            # tenant_data_str = yaml.safe_dump({tenant_name: tenant_data})  # Convert to string
            # client.put(tenant_name, tenant_data_str)  # Update database
            # # tenant_data = yaml.safe_dump(tenant_data)
    # tenant_data = {tenant_name: tenant_data}
    client.put(tenant_name, str(tenant_data))

if __name__ == "__main__":

    example_key = "netflix"  # Example key for tenant data

    # Retrieve data from etcd
    value, _ = client.get(example_key)
    if value:
        tenant_data = eval(value.decode())  #yaml.safe_load(value.decode())
        print("tenant_data = ", tenant_data)
        check_and_update_state(example_key, tenant_data)
    else:
        print(f"No data found for key: {example_key}")














# import yaml
# from ansible_runner import run
# import os

# # Define states
# states = ['requested', 'processing', 'active', 'terminate']

# # Function to run Ansible playbook
# def run_playbook(filename, vars_dict):
#     config = {
#         'private_data_dir': './',
#         'playbook': filename,
#         'extravars': vars_dict
#     }
#     result = run(**config)
#     return result

# # Function to update database
# def update_db(data):
#     with open(database, 'w') as f:
#         yaml.dump(data, f, sort_keys=False)
#     return

# # Function to create VPC
# def create_vpc(vpc):
#     # Replace with actual playbook and vars
#     run_playbook('create_vpc.yaml', {'vpc_name': vpc['name']})
#     return

# # Function to create Subnet
# def create_subnet(subnet):
#     # Replace with actual playbook and vars
#     run_playbook('create_subnet.yaml', {'subnet_name': subnet['name']})
#     return

# # Function to create VM
# def create_vm(vm):
#     # Replace with actual playbook and vars
#     run_playbook('create_vm.yaml', {'vm_name': vm['name']})
#     return

# # Function to check and handle requests
# def check_requests(data):
#     for tenant in data['tenants']:
#         for vpc in tenant['vpcs']:
#             if vpc['state'] == states[0]:
#                 # Process VPC creation
#                 create_vpc(vpc)
#                 vpc['state'] = states[2]  # Update state to 'active'
#                 update_db(data)  # Update database

#                 for subnet in vpc['subnets']:
#                     if subnet['state'] == states[0]:
#                         # Process Subnet creation
#                         create_subnet(subnet)
#                         subnet['state'] = states[2]  # Update state to 'active'
#                         update_db(data)  # Update database

#                         for vm in subnet['VMs']:
#                             if vm['state'] == states[0]:
#                                 # Process VM creation
#                                 create_vm(vm)
#                                 vm['state'] = states[2]  # Update state to 'active'
#                                 update_db(data)  # Update database

# if __name__ == '__main__':
#     # Read YAML data from file
#     with open('customer_input_infra.yaml', 'r') as f:
#         data = yaml.safe_load(f)
    
#     # Check and handle requests
#     check_requests(data)
