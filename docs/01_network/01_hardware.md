# Hardware & Physical Infrastructure

## 1. Overview
This document defines the physical layer (OSI Layer 1) of the Packetflow Homelab.  
It covers hardware specifications, physical cabling, and port assignments across the core infrastructure.  

## 2. Hardware Inventory

| Device Role | Make / Model | Hostname | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Router / Firewall** | Fortinet FortiGate 40F | `FW01` | Main internet gateway and security appliance. |
| **Core Switch** | Ubiquiti EdgeSwitch 8 PoE | `ALS01` | Managed L2 switch providing PoE to APs and connectivity to servers. |
| **Access Point** | MikroTik hAP ac lite | `AP01` | Dual-concurrent Access Point. **Used for learning MikroTik RouterOS.** |
| **Compute** | Generic Servers | *Various* | Hypervisors and storage servers. |

Note: All hosts are part of the `lab.internal.packetflow.be` domain. So `FW01` can be reached internaly as `fw01.lab.internal.packetflow.be`.


## 3. Physical Topology
The network centers around a "Core Rack" configuration where the FortiGate handles WAN and the EdgeSwitch handles internal distribution.

**[Image Placeholder: Physical Topology Diagram]**

## 4. Cabling & Port Map

### FortiGate 40F
| Port | Type | Connected Device | Notes |
| :--- | :--- | :--- | :--- |
| WAN | RJ45 | ISP Modem | Public IP via DHCP/PPPoE |
| 1 | RJ45 | AP01 | HAP AC Lite currently used as AP |
| 2 | RJ45 | ALS01 | Main Trunk Link (Carries all VLANs) |
| 3 | RJ45 | *Reserved* | Emergency Management / Direct Access |

### Ubiquiti EdgeSwitch 8 PoE
| Port | Profile | Connected Device | PoE Mode |
| :--- | :--- | :--- | :--- |
| 1 | Trunk | **uplink to FW01** | POE+ (0W) |
| 2-8 | Access/Trunk | Servers / IoT | *As needed* |

### MikroTik hAP ac lite (AP01)
*Radio Configuration:*
- **wlan2 (5GHz):** High-speed clients
