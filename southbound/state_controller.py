import etcd3
import subprocess
from ansible_runner import run
import yaml
import sys

client = etcd3.client()

# Function to run Ansible playbook
def run_playbook(filename, vars_dict):
    config = {
        'private_data_dir': './',
        'playbook': filename,
        'extravars': vars_dict
    }
    result = run(**config)
    return

def create_infra_resources(tenant_name, tenant_data):
    run_playbook('deploy_infra.yaml', {'tenant_name': [tenant_name]})
    return

def create_VM_resources(tenant_name, tenant_data):
    run_playbook('deploy_VMs.yaml', {'tenant_name': [tenant_name]})
    return

def create_cdn_resources(tenant_name, tenant_data):
    run_playbook('deploy_cdn.yaml', {'tenant_name': [tenant_name]})
    return

def check_and_update_VM_state(tenant_name, tenant_data):
    for vpc in tenant_data[tenant_name]['vpcs']:
        if vpc['VMs_state'] == 'requested':                             
            create_VM_resources(tenant_name, tenant_data)
            vpc['VMs_state'] = 'active'
        break
    client.put(tenant_name, str(tenant_data))

def check_and_update_tenant_state(tenant_name, tenant_data):
    if  tenant_data[tenant_name]['state'] == 'requested':
        create_infra_resources(tenant_name, tenant_data)
        tenant_data[tenant_name]['state'] = 'active'
    client.put(tenant_name, str(tenant_data))

def check_and_update_cdn(tenant_name, tenant_data):
    if  tenant_data[tenant_name]['cdn']['state'] == 'requested':
        create_cdn_resources(tenant_name, tenant_data)
        tenant_data[tenant_name]['cdn']['state'] = 'active'
    client.put(tenant_name, str(tenant_data))

if __name__ == "__main__":

    # example_key = "netflix" 
    example_key = sys.argv[1]

    # Retrieve data from etcd
    value, _ = client.get(example_key)
    if value:
        tenant_data = eval(value.decode())  
        print("tenant_data = ", tenant_data)
        # check_and_update_tenant_state(example_key, tenant_data)
        # check_and_update_VM_state(example_key, tenant_data)
        check_and_update_cdn(example_key, tenant_data)
    else:
        print(f"No data found for key: {example_key}")


