# RapidServe
CDNaaS

Step 1:
Dependencies:
  1. setup the etcd db by following the etcd setup document
  2. Install etcd: sudo apt install python3-etcd
  3. sudo apt install python3-pyyaml
  4. sudo apt install python3-ansible-runner
  5. sudo apt install python3-netaddr
  6. sudo apt install dnsmasq
  7. Upgrade ansible collections: ansible-galaxy collection install ansible.netcommon --upgrade


Step 2: run verify_input.py to validate the input given by the tenant
        python3 verify_input.py

Step 3: run the input_parser.py to parse the input yaml file and save the data into etcd db
        python3 input_parser.py

Step 4: run the state_controller.py to check the state of respective field and deploy the requried resource by running the respective playbook
        python3 state_controller.py <tenant_name>

Step 5: run the implement_dns.yaml to install BIND9 and create DNS functionality on the server. Note that the IP address corresponding to the DNS server VM should be provided in the inventory_dns.ini file. 
        sudo ansible-playbook -i inventory_dns.ini implement_dns.yaml -e  "tenant_name=<tenant-name>"

