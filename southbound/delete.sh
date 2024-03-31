#!/bin/bash
sudo ip link delete n1_sub1_br type bridge
sudo ip link delete n1_sub2_br type bridge
sudo ip link delete n2_sub1_br type bridge
sudo ip link delete n2_sub2_br type bridge

# Deleting OVS bridges
sudo ovs-vsctl del-br n1_sub2_br
sudo ovs-vsctl del-br n1_sub1_br
sudo ovs-vsctl del-br n2_sub2_br
sudo ovs-vsctl del-br n2_sub1_br

# Deleting virtual ethernet (veth) pairs
sudo ip link delete n1_sub2_veth0
sudo ip link delete n2_sub2_veth0
sudo ip link delete n2_sub1_veth0
sudo ip link delete n1_sub1_veth0

# Deleting network namespaces
sudo ip netns delete netflix1
sudo ip netns delete netflix2

# Deleting additional veth interfaces
sudo ip link delete netflix2_veth0
sudo ip link delete netflix1_veth0
