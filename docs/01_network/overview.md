# Network Infrastructure

## 1. Overview
This document details the network topology, addressing schemes, and security policies for the **Packetflow Homelab**.  
The network provides an (un)stable experimental environment while also serving my Home WiFi.  
It's subject to many changes and should **not** be considered a production environment.

**Key Stats:**  
- **Primary Domain:** `packetflow.be` (Subdomain: `lab.internal.packetflow.be`)  
- **Router/Firewall:** FortiGate 40F  
- **Core Switch:** Ubiquiti EdgeSwitch 8 PoE  
- **Wireless:** MikroTik hAP ac lite  
- **Site CIDR:** `10.10.0.0/16` (Home)  
- **Remote Branch Office CIDR:** `10.20.0.0/16` (Not yet implemented)  
---

## 2. Basic Principles
The design and maintenance of this network adhere to the following core principles:

1.  **Strict Segmentation:**  
    - The "Home office" network (`10.10.0.0/16`) is distinct from the reserved "Remote branch office" range (`10.20.0.0/16`).   
    - All VLANs are separated from each other.  
2.  **Default Deny security policy:**  
    - The firewall operates on a "deny-by-default" basis.  
    - Traffic is only permitted if explicitly defined in the policy table; the default action is `DROP`.  
3.  **Management isolation:**  
    - Management interfaces (Switching, Routing, IPMI) are restricted to **VLAN 99**.  
4.  **Physical security:**  
    - Unused switch ports and the native VLAN on trunks are assigned to **VLAN 666 (Blackhole)** to prevent unauthorized physical access.  

---

## 3. Network Topology

### Layer 1: Physical Topology
The physical connection diagram without any IP addresses.

**[Image Placeholder: Physical Topology Diagram]**

### Layer 2: Data Link Topology
The data link layer configuration, including VLANs.

**[Image Placeholder: Data Link Topology Diagram]**

