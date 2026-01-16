# Security & Policies

## 1. Overview
The security posture follows a **Positive Security Model**: everything is blocked by default unless explicitly allowed. The **FortiGate 40F** acts as the Zone-Based Firewall.

## 2. Firewall Zones
Traffic is grouped by source interface/VLAN to simplify policy management.

- **Trusted:** VLAN 10 (Home), VLAN 20 (Guest)
- **Untrusted:** WAN (Internet)
- **Management:** VLAN 99
- **Emergency:** LAN3 (Physical port for recovery)

## 3. Firewall Policies
The following policies are currently active on the FortiGate:

| ID | Name | Source | Destination | Action | NAT | Services | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **4** | `Allow default VLANs to BSI and mail` | VLAN 10, VLAN 20 | `virtual-wan-link` (Internet) | **ACCEPT** | Enabled | ICMP, HTTP/S, Email, ScreenConnect | General internet access for users. |
| **5** | `Allow mgmt to everything` | VLAN 99 | ANY | **ACCEPT** | Enabled | ALL_ICMP, SNMP, SSH, DNS, NTP, etc. | Unrestricted admin access. |
| **3** | `Allow emergency to internet` | lan3 | `virtual-wan-link` | **ACCEPT** | Enabled | ALL | Emergency internet access. |
| **2** | `Allow emergency to everywhere` | lan3 | `mgmt` | **ACCEPT** | Disabled | ALL | Emergency router access. |

## 4. Security Profiles
- **SSL Inspection:** Default `certificate-inspection` (no decryption) is applied to most basic policies.
- **Deep Packet Inspection:** Not currently enforced globally to preserve privacy/performance on the 40F.
