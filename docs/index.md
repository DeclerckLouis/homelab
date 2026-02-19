# Packetflow Homelab website

## Welcome
Welcome to the documentation for the **Packetflow Homelab**.  
This project serves as a practical testing ground for network engineering concepts,  
specifically focusing on **network documentation** topics (See [Documentation](./homelab/01_network/01_physical.md)) and **small projects** (See [Blog](blog/index.md)).  
It's subject to many changes and should **not** be considered production-grade. (Although that's what I aim for with the [Documentation](./homelab/01_network/01_physical.md))  

## Lab Overview

- **Primary Router:** Fortinet FortiGate 40F (handling Routing, Security, SD-WAN).  
- **Core Switching:** Ubiquiti EdgeSwitch 8 PoE (handling VLANs, PoE).  
- **Wireless/Access:** MikroTik hAP ac lite (handling WiFi, Bridge Filtering).  
- **Servers:**  One Raspberry Pi 4, One Raspberry Pi 5
- **Workstations:** One Windows 10 Desktop, one Red Hat Enterprise Linux 10 Laptop  

## Network Documentation Structure
The documentation is currently focused on networking, and has been structured into sections within the **Network** module:

### 1. [Physical Layout](homelab/01_network/01_physical.md)  
Detailed inventory of all physical devices, cabling maps, and the physical topology showing how the ISP Modem, FortiGate, and downstream switches connect.

### 2. [Logical Layout](homelab/01_network/02_logical.md)  
Defines the **Logical Topology**.

- **VLANs:** Segmentation for Default, Guest, Servers, DMZ, and Management.  
- **IPv6 Strategy:** Explains the decision to use **Unique Local Addressing (ULA)** (`fdb1:6575:ad8a::/48`) due to ISP (modem) constraints.
- **WAN/SD-WAN:** Configuration of the `virtual-wan-link` interface.

### 3. [Device Decisions](homelab/01_network/03_device_decisions.md)  
Covers **routing, switching, and configuration standards**.

- **Switching:** 802.1Q Trunks, Native VLAN security, and Bridge VLAN Filtering on MikroTik.  
- **Routing:** Inter-VLAN routing and IPv6 Router Advertisements (RA).
- **Standards:** Interface configuration templates and naming conventions.

### 4. [Security](homelab/01_network/04_security.md)  
Documents the **Security policies** used.  

- **Zones:** Trusted vs Untrusted vs Management.  
- **Policies:** Specific firewall rules allowing traffic while blocking inter-VLAN access by default.  

### 5. [Wireless](homelab/01_network/06_wireless.md)  
Design decisions for the `Declerck-Cardon` SSID, frequency planning, and security standards. 


## Future Plans
- Add another hAP ac lite to act as second switch.
- Add another router to act as remote/branch office router.
- Replace my current Telenet modem with a new one to support IPv6 Global Unicast Addressing in all VLANs.  
    So far i've managed to get it working in one VLAN.  
- Setup a DNS server with dynamic DNS.

## Disclaimer  
The documentation is written/formatted with the help of Google Gemini.  
The decisions made are based on my own knowledge and experience. 
