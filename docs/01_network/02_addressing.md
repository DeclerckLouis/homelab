# Network Addressing & VLANs

## 1. Overview
This document details the logical segmentation of the network, including VLAN assignments, IPv4 subnetting, and the IPv6 addressing strategy.

## 2. VLAN Configuration
The network follows a strict segmentation policy using hierarchical supernets and VLANs.

### 2.1. Supernets
| Supernet | Name | Description |
| :--- | :--- | :--- |
| `10.0.0.0/8` | **PacketFlow** | Global Supernet |
| `10.10.0.0/16` | **Home Office** | Primary Site (Lab & Residence) |
| `10.20.0.0/16` | **Branch Office** | Remote Site |

### 2.2. VLAN Assignment
| VLAN ID | Name | Home Office (10.10.x.x) | Branch Office (10.20.x.x) | IPv6 Subnet | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **10** | `Home` | `10.10.10.0/24` | `10.20.10.0/24` | `...:10::/64` | **Default Trusted Network.** "Office" devices. |
| **20** | `Guest` | `10.10.20.0/23` | `10.20.20.0/23` | `...:20::/64` | **Guest Network.** Personal devices and WiFi - Isolated internet access. |
| **30** | `Servers` | `10.10.30.0/24` | N/A | `...:30::/64` | **Servers.** Raspberry pi's, internal services hosted in docker containers and VMs. |
| **35** | `DMZ` | `10.10.35.0/24` | N/A | `...:35::/64` | **DMZ.** Public facing services. |
| **99** | `MGMT` | `10.10.99.0/24` | `10.20.99.0/24` | `...:99::/64` | **Management.** Management of Network Infrastructure. |
| **666** | `Blackhole`| N/A | N/A | N/A | **Dead VLAN.** Used for Native VLAN security. |

## 3. IPv6 Strategy
### 3.1. Design Choices
Due to ISP constraints and difficulties with robust Prefix Delegation (PD) / GUA stability, the network currently utilizes **Unique Local Addresses (ULA)** for consistent internal addressing.

### 3.2. Prefix Assignment
- **ULA Prefix:** `fdb1:6575:ad8a::/48`
- **Allocation Method:** Static assignment per VLAN.

### 3.3. Subnetting Plan
| VLAN | IPv6 Subnet |
| :--- | :--- |
| **10** (Home) | `fdb1:6575:ad8a:10::/64` |
| **20** (Office) | `fdb1:6575:ad8a:20::/64` |
| **30** (Servers) | `fdb1:6575:ad8a:30::/64` |
| **35** (DMZ) | `fdb1:6575:ad8a:35::/64` |
| **99** (Mgmt) | `fdb1:6575:ad8a:99::/64` |

## 4. Key Static IPs (Legacy IPv4)
| Device | IP Address | VLAN | Notes |
| :--- | :--- | :--- | :--- |
| **FortiGate 40F** | `10.10.10.1` | 10 | Primary Gateway |
| **FortiGate 40F** | `10.10.99.1` | 99 | Primary Gateway Management|
| **EdgeSwitch** | `10.10.99.2` | 99 | Core Switch Management |
| **AP01 (MikroTik)** | `DHCP` | 99 | Currently dynamic |

## 5. Troubleshooting & Issues
### 5.1. IPv6 GUA / SLAAC Failure
**Issue:** Initial attempts to configure Global Unicast Addresses (GUA) via SLAAC failed.
**Root Cause:** ISP modem/connection constraints prevented proper Prefix Delegation or routing of the delegated prefix.
**Resolution:** Switched to ULA (`fdb1:6575:ad8a::/48`) to ensure stable internal IPv6 connectivity and addressing, allowing for learning/testing of IPv6 mechanisms (RA, DHCPv6) independent of the ISP connection.
