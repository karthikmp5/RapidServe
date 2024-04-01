#!/bin/bash

# Define an array of VM names
#VM_NAMES=("netflix111" "netflix121" "netflix211" "netflix221")
VM_NAMES=("NF_US_VM1" "NF_US_VM2" "NF_JP_VM1" "NF_JP_VM2")

# Loop through the VM names array
for VM_NAME in "${VM_NAMES[@]}"; do
    echo "Destroying VM: $VM_NAME"
    virsh destroy "$VM_NAME"
    virsh undefine "$VM_NAME"
    echo "Removing VM image directory: /var/lib/libvirt/images/$VM_NAME"
    sudo rm -rf "/var/lib/libvirt/images/$VM_NAME"
done

echo "All specified VMs have been destroyed and their image directories removed."

