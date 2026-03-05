# Security and policies

## 1. Overview

The **FortiGate 40F** acts as a stateful firewall.  
An **implicit deny rule** applies at the end of the policy list.  

## 2. Firewall zones (not used)

!!! note "Not used"
    Due to the VLANs already being used in the hardware switch, you cannot add them to zones.
    You might reconsider this later or redo the whole FortiGate setup for a firewall-focused lab.

- **LAN_Trusted:** VLAN 10 (Default)  
- **LAN_Guest:** VLAN 20 (Guest)  
- **SRV_Servers:** VLAN 30 (Servers)  
- **SRV_DMZ:** VLAN 35 (DMZ)  
- **WAN_Internet:** WAN (Internet)  
- **LAN_MGMT:** VLAN 99 (Management), INT03 (Emergency)  

!!! note "Currently 2 Linux servers and no printers"
    Currently running 2 Linux servers (Grafana and Netbox, neither in the DMZ).
    Future deployments include HAProxy for the DMZ.  
    An IoT VLAN (VLAN31 IoT) with printers has its own zone.

## 3. Firewall Policies
The following policies are currently active on the FortiGate:

| Name                                 | From    | To                 | Source            | Destination | Action     | NAT      | Services                           | Notes                               |
| :----------------------------------- | :------ | :----------------- | :---------------- | :---------- | :--------- | :------- | :--------------------------------- | :---------------------------------- |
| `Allow default VLAN to BSI and mail` | VLAN 10 | `virtual-wan-link` | (4)VLAN10 address | (4)all      | **ACCEPT** | Enabled  | ICMP, HTTP/S, Email, ScreenConnect | General internet access for users.  |
| `Allow guest VLAN to BSI and mail`   | VLAN 20 | `virtual-wan-link` | (4)VLAN20 address | (4)all      | **ACCEPT** | Enabled  | ALL_ICMP, HTTP/S, Email            | General internet access for guests. |
| `Allow mgmt to internet with NAT`    | VLAN 99 | `virtual-wan-link` | (4)VLAN99 address | (4)all      | **ACCEPT** | Enabled  | ALL                                | Unrestricted admin access.          |
| `Allow mgmt to everywhere`           | VLAN 99 | ANY                | (4)VLAN99 address | (4)all      | **ACCEPT** | Disabled | ALL                                | Unrestricted admin access.          |
| `Allow emergency internet access`    | INT03   | `virtual-wan-link` | (4)all            | (4)all      | **ACCEPT** | Enabled  | ALL                                | Emergency internet access.          |
| `Allow emergency to everywhere`      | INT03   | `down (mgmt)`      |                   |             | **ACCEPT** | Disabled | ALL                                | Emergency router access.            |

## 4. Security Profiles
- **SSL Inspection:** The default `certificate-inspection` setting (no decryption) applies to most basic policies.
- **Deep Packet Inspection:** Not currently enforced globally to preserve privacy/performance on the 40F.
