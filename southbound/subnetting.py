import ipaddress
import os

# File to store the allocated subnets
storage_file = 'allocated_subnets.txt'

def get_next_subnet(base_subnet):
    """
    Calculate the next /30 subnet that has not been allocated yet.
    """
    base_subnet = ipaddress.ip_network(base_subnet, strict=False)
    allocated_subnets = load_allocated_subnets()

    for sn in base_subnet.subnets(new_prefix=30):
        if str(sn) not in allocated_subnets:
            allocated_subnets.add(str(sn))
            save_allocated_subnets(allocated_subnets)
            return sn
    
    # If we reach here, it means all /30 subnets in the /24 range have been allocated.
    return None

def save_allocated_subnets(subnets):
    """Save the allocated subnets to a file."""
    with open(storage_file, 'w') as f:
        for subnet in subnets:
            f.write(f"{subnet}\n")

def load_allocated_subnets():
    """Load the allocated subnets from a file."""
    if os.path.exists(storage_file):
        with open(storage_file, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def main():
    next_subnet = get_next_subnet('192.168.100.0/24')
    if next_subnet:
        print(f"{next_subnet}")
    else:
        print("No more /30 subnets available in the /24 range.")

if __name__ == "__main__":
    main()


