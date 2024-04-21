import yaml
import subprocess
from ansible_runner import run
import ipaddress
import sys
import os

result = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
base_directory = result.decode('utf-8').strip()

def select_inventory(vpc_name):
    if vpc_name.endswith(('in', 'ja')):
        return os.path.join(base_directory, 'southbound', 'host_inventory_asia.ini')
    elif vpc_name.endswith(('ge', 'fr')):
        return os.path.join(base_directory, 'southbound', 'host_inventory_europe.ini')

# Function to run Ansible playbook
def run_playbook(filename, vars_dict, vpc_name):
    inventory_file = select_inventory(vpc_name)
    config = {
        'private_data_dir': './',
        'playbook': filename,
        'extravars': vars_dict,
        'verbosity': 3,
        'inventory': inventory_file
        }
    result = run(**config)
    return result

def calculate_ip(tenant_name, tenant_data):
    for subnet in tenant_data['subnets']:
        cidr = subnet['CIDR']
        
        # Extract the network address and prefix length from the CIDR
        network = ipaddress.ip_network(cidr)
        ip = str(network.network_address + 1)  # IP is the first address in the CIDR block
        dhcp_start = str(network.network_address + 2)  # DHCP start is the second address
        dhcp_end = str(network.broadcast_address - 1)  # DHCP end is the last but one address

        # Add the new fields to the subnet
        subnet['ip'] = ip
        subnet['dhcp_start'] = dhcp_start
        subnet['dhcp_end'] = dhcp_end
    save_updated_tenant_data(tenant_name, tenant_data)

def get_subnet():
    # Run the subnetting script and capture the output
    result = subprocess.run(['python3', 'subnetting.py', '192.168.4.0/24'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()  # Ensure whitespace is trimmed
    else:
        raise Exception("Failed to get subnet: " + result.stderr)

def check_and_create_vpc(tenant_name, tenant_data):
    for vpc in tenant_data['vpcs']:
        if vpc['vpc_state'] == 'requested':
            vars_dict = {
                'tenant_name': tenant_name,
                'tenant_data': tenant_data,
                'vpc_name': vpc['name']
            }
            playbook_path = os.path.join(base_directory, 'southbound', 'deploy_vpc.yaml')
            result = run_playbook(playbook_path, vars_dict, vpc['name'])
            if result.rc == 0:
                tunnel_subnet = get_subnet()
                vars_dict = {
                'tenant_name': tenant_name,
                'tenant_data': tenant_data,
                'vpc_name': vpc['name'],
                'vpc_subnet_output': tunnel_subnet
                }
                playbook_path = os.path.join(base_directory, 'southbound', 'create_tunnels.yaml')
                result = run_playbook(playbook_path, vars_dict, vpc['name'])
                if result.rc == 0:
                    vpc['vpc_state'] = 'active'
                    save_updated_tenant_data(tenant_name, tenant_data)
                else:
                    print("Error occurred while creating tunnels.")
                    sys.exit(1)
            else:
                print("Error occurred while creating VPC resources.")
                sys.exit(1)

def check_and_create_subnet(tenant_name, tenant_data):
    for subnet in tenant_data['subnets']:
        if subnet['subnet_state'] == 'requested':
            vars_dict = {
                'tenant_name': tenant_name,
                'tenant_data': tenant_data,
                'subnet_name': subnet['name'],
                'vpc_name': subnet['vpc'],
                'subnet_CIDR': subnet['CIDR'],
                'ip': subnet['ip'],
                'dhcp_start': subnet['dhcp_start'],
                'dhcp_end': subnet['dhcp_end']
            }
            playbook_path = os.path.join(base_directory, 'southbound', 'deploy_subnet.yaml')
            result = run_playbook(playbook_path, vars_dict, subnet['vpc'])
            if result.rc == 0:
                subnet['subnet_state'] = 'active'
                save_updated_tenant_data(tenant_name, tenant_data)
            else:
                print("Error occurred while creating subnet resources.")
                sys.exit(1)

def check_and_create_containers(tenant_name, tenant_data):
    for container in tenant_data['containers']:
        if container['container_state'] == 'requested':
            gateway_subnet = container['subnets'][0]
            for subnet in tenant_data['subnets']:
                if subnet['name'] == gateway_subnet:
                    container_gateway_ip = subnet['ip']
                    vars_dict = {
                        'tenant_name': tenant_name,
                        'container_name': container['name'],
                        'vpc_name': container['vpc'],
                        'subnets': container['subnets'],
                        'container_gateway_ip': container_gateway_ip
                    }
                    playbook_path = os.path.join(base_directory, 'southbound', 'deploy_con.yaml')
                    result = run_playbook(playbook_path, vars_dict, container['vpc'])

            if result.rc == 0:
                container['container_state'] = 'active'
                save_updated_tenant_data(tenant_name, tenant_data)
            else:
                print("Error occurred while creating container resources.")
                sys.exit(1)

def save_yaml(data):
    config_path = os.path.join(base_directory, 'config.yaml')
    with open(config_path, "w") as file:
        yaml.safe_dump(data, file, sort_keys=False)

def read_yaml():
    try:
        config_path = os.path.join(base_directory, 'config.yaml')
        with open(config_path, "r") as file:
            data = yaml.safe_load(file)
            if data is None:  # If file is empty, return an empty dictionary
                return {'tenants': []}
            return data
    except FileNotFoundError:
        return {'tenants': []}

def fetch_tenant_info(org_name):
    data = read_yaml()
    if data is None:
        print("Failed to read data.")
        return
    # Find the specific tenant based on the organization name
    tenant_data = next((tenant for tenant in data.get('tenants', []) if tenant['name'] == org_name), None)
    if tenant_data is None:
        print(f"No data found for the organization named {org_name}. Please check the organization name and try again.")
        return
    # Print the data in a structured format
    print("Fetching data for organization:", org_name)
    return(tenant_data)

def save_updated_tenant_data(tenant_name, tenant_data):
    full_data = read_yaml()  # Load the full structure
    for tenant in full_data['tenants']:
        if tenant['name'] == tenant_name:
            update_tenant(tenant, tenant_data)  # Update the tenant info in the full data
    save_yaml(full_data)


def update_tenant(original, updated):
    # Helper function to update tenant info in the full list
    original.update(updated)

if __name__ == "__main__":
    tenant_name = sys.argv[1] if len(sys.argv) > 1 else "default_tenant"
    # tenant_data = {"tenant": fetch_tenant_info(tenant_name)}
    tenant_data = fetch_tenant_info(tenant_name)
    if tenant_data:
        print("Tenant data loaded successfully.")
        # print(yaml.dump({"tenant": tenant_data}, sort_keys=False))
        # print(yaml.dump(tenant_data, sort_keys=False))
        calculate_ip(tenant_name, tenant_data)
        tenant_data = fetch_tenant_info(tenant_name)
        print(yaml.dump({"tenant": tenant_data}, sort_keys=False))
        check_and_create_vpc(tenant_name, tenant_data)
        check_and_create_subnet(tenant_name, tenant_data)
        check_and_create_containers(tenant_name, tenant_data)
    else:
        print(f"No data found for tenant: {tenant_name}")
