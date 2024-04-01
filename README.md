# RapidServe
CDNaaS

setup the etcd db

run the input_parser.py

run the state_controller.py <tenant_name>

sudo ansible-playbook -i inventory_dns.ini implement_dns.yaml -e "tenant_name=netflix"
