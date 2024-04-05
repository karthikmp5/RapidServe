#!/bin/bash
sudo ip link delete NF_US_S1_br type bridge
sudo ip link delete NF_US_S2_br type bridge
sudo ip link delete NF_JP_S1_br type bridge
sudo ip link delete NF_JP_S2_br type bridge

# Deleting OVS bridges
# sudo ovs-vsctl del-br n1_sub2_br
# sudo ovs-vsctl del-br n1_sub1_br
# sudo ovs-vsctl del-br n2_sub2_br
# sudo ovs-vsctl del-br n2_sub1_br

# Deleting virtual ethernet (veth) pairs
sudo ip link delete NF_US_S1_veth0
sudo ip link delete NF_US_S2_veth0
sudo ip link delete NF_JP_S1_veth0
sudo ip link delete NF_JP_S2_veth0

# Deleting network namespaces
sudo ip netns delete NF_US
sudo ip netns delete NF_JP

# Deleting additional veth interfaces
sudo ip link delete NF_US_veth0
sudo ip link delete NF_JP_veth0