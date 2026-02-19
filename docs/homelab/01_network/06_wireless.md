# Wireless Configuration

## 1. Overview
Wireless connectivity is provided by a **MikroTik HAP ac Lite** that I had laying around.  
The WiFi logic is separate from the routing core (FortiGate), operating in "Bridge AP" mode.  

## 2. Access Points
| Device | Model | Location | Management IP |
| :--- | :--- | :--- | :--- |
| **AP01** | MikroTik hAP ac lite | Central | `10.10.99.x` (DHCP) |

## 3. SSIDs & Frequency Planning

| SSID | Band | Frequency | Channel Width | Target VLAN | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Declerck-Cardon** | 5 GHz | *Auto* | 40 MHz | **20** (Guest) | Any guest clients |

!!! note "Note"
    This device currently serves the home wifi, this is done to generate some "real" traffic on the network.  
    While not necessarily best practice, it allows me to spot issues faster.

## 4. Security Decisions
- **Authentication:** WPA2-PSK (AES-CCMP).
- **Key:** An easy-to-remember password given to guests.
- **Isolation:** Client-to-Client forwarding is allowed by default on the AP Bridge, but Inter-VLAN traffic is blocked by the Firewall.

## 5. Implementation Logic (MikroTik)
The generic MikroTik implementation places all wireless clients into a specific VLAN tag at the AP ingress.
- **PVID/VLAN Mapping:** `wlan1` and `wlan2` interfaces are set with PVID=20.
- **Bridge Filtering:** The bridge tags frames from these interfaces with VLAN 20 before sending them up the trunk to the Core Switch.
