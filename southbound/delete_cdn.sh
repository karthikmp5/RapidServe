#!/bin/bash

# Configuration variables
VPC_NAME="origin_ns"
BRIDGE_NAME="origin_bridge"
VM_NAME="origin_server_vm"
IMAGE_DIR="/var/lib/libvirt/images/$VM_NAME"

# Networking - Corrected as per playbook variables
VETH_NS_TO_ROOT="origin_ns"        # Adjusted to match playbook
VETH_ROOT_TO_NS="origin_root"      # Adjusted to match playbook
VETH_NS_TO_BRIDGE="origin_nsbridge"   # Adjusted to match playbook
VETH_BRIDGE_TO_NS="origin_bridgens"   # Adjusted to match playbook

# Stop and undefine the VM
echo "Stopping VM..."
virsh destroy $VM_NAME 2>/dev/null
echo "Undefining VM..."
virsh undefine $VM_NAME 2>/dev/null

# Delete VM images and cloud-init ISO
echo "Removing VM images and cloud-init ISO..."
rm -rf $IMAGE_DIR

# Delete the veth pairs - Adjusted to match playbook variables
echo "Deleting veth pairs..."
ip link delete $VETH_ROOT_TO_NS 2>/dev/null
ip netns exec $VPC_NAME ip link delete $VETH_NS_TO_BRIDGE 2>/dev/null

# Delete the bridge
echo "Deleting the bridge..."
ip link set $BRIDGE_NAME down 2>/dev/null
ip link delete $BRIDGE_NAME type bridge 2>/dev/null

# Delete the network namespace
echo "Deleting the network namespace..."
ip netns delete $VPC_NAME 2>/dev/null

echo "Cleanup complete."
