# Packetflow Homelab Documentation repo

## Welcome  

Welcome to the documentation for the **Packetflow Homelab**.  
This project serves as a practical testing ground for network engineering concepts, automation snippets, and other IT-related projects.  

---
**You can read the actual documentation over at [Packetflow Lab](https://lab.packetflow.be)**  
--- 

## Lab Overview
The homelab is designed to mimic a small enterprise network with distinct layers for Core, Distribution, and Access.

- **Primary Router:** Fortinet FortiGate 40F (handling Routing, Security, SD-WAN).
- **Core Switching:** Ubiquiti EdgeSwitch 8 PoE (handling VLANs, PoE).
- **Wireless/Access:** MikroTik hAP ac lite (handling WiFi, Bridge Filtering).

## Documentation Structure
The documentation is currently focused on networking, and has been structured into sections within the **Network** module:

### 1. [Hardware](./docs/homelab/01_network/01_hardware.md)  
Detailed inventory of all physical devices, cabling maps, and the physical topology showing how the ISP Modem, FortiGate, and downstream switches connect.

### 2. [Addressing](./docs/homelab/01_network/02_addressing.md)  
Defines the **Logical Topology**.

- **VLANs:** Segmentation for Default, Guest, Servers, DMZ, and Management.  
- **IPv6 Strategy:** Explains the decision to use **Unique Local Addressing (ULA)** (`fdb1:6575:ad8a::/48`)  
    due to ISP (modem) constraints, ensuring stable internal IPv6 routing and learning opportunities.

### 3. [Routing & Switching](./docs/homelab/01_network/03_routing_switching.md)  
Covers **routing and switching** configuration and decisions inside the network.

- **Switching:** 802.1Q Trunks, Native VLAN security, and Bridge VLAN Filtering on MikroTik.  
- **Routing:** Inter-VLAN routing and IPv6 Router Advertisements (RA).

### 4. [Security](./docs/homelab/01_network/04_security.md)  
Documents the **Security policies** used.  

- **Zones:** Trusted vs Untrusted vs Management.  
- **Policies:** Specific firewall rules allowing traffic (e.g., VLAN 10/20 to Internet) while blocking inter-VLAN access by default.  

### 5. [SD-WAN](./docs/homelab/01_network/05_sd_wan.md)  
Configuration of the `virtual-wan-link` interface to abstract WAN connectivity and prepare for future multi-path scenarios.  

### 6. [Wireless](./docs/homelab/01_network/06_wireless.md)  
Design decisions for the `Declerck-Cardon` SSID, frequency planning, and security standards.  


## Future Plans
- Add another hAP ac lite to act as second switch.
- Add another router to act as remote/branch office router.
- Replace my current Telenet modem with a new one to support IPv6 Global Unicast Addressing in all VLANs.  
    So far i've managed to get it working in one VLAN.  
- Setup a DNS server with dynamic DNS.

## Disclaimer  
The documentation is written with the help of Google Gemini.  
The decisions made are based on my own knowledge and experience. 
