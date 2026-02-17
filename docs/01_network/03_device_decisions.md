# Basic Device Decisions

## 1. Design Rationale
The core principles driving device configuration are:
1.  **Automation Friendly:** Configurations should be standardized to allow for future automation (e.g., Ansible/Terraform).
2.  **Security by Default:** Deny-all policies, minimal open ports, and strict VLAN segmentation.
3.  **Consistency:** Naming conventions and IP schemes must be identical across devices and sites.

## 2. Software Standards
To ensure stability and feature compatibility, the following software versions are targeted:

| Device | Software | Target Version | Update Policy |
| :--- | :--- | :--- | :--- |
| **FortiGate 40F** | FortiOS | 7.2.x (Mature) | Manual update after backing up config. |
| **EdgeSwitch** | EdgeSwitch Firmware | Latest Stable | As needed for security patches. |
| **MikroTik hAP** | RouterOS | v7.x (Stable) | Auto-update disabled; manual review required. |

## 3. Configuration Standards

### 3.1. Interface Configuration (FortiGate)
Interfaces follow a strict template for IPv4 and IPv6 dual-stack connectivity.

```bash title="Example: VLAN 10"
config system interface
    edit "VLAN10"
        set vdom "root"
        set ip 10.10.10.1 255.255.255.0
        set allowaccess ping
        set alias "VLAN Default"
        set role lan
        config ipv6
            set ip6-address fdb1:6575:ad8a:10::1/64
            set ip6-allowaccess ping
            config ip6-extra-addr
                edit fe80::10:1/64 #(1)!
                next
            end
            set ip6-send-adv enable
            set ip6-other-flag enable
        end
        set vlanid 10
    next
end
```

1.  **Link Local Address:** Manually set to `fe80::[VLAN_ID]:1` for consistency and ease of future troubleshooting.

### 3.2. Switching Logic (Ubiquiti EdgeSwitch)
- **VLANs:** Must be defined in the VLAN database.
- **Trunking:** Uplinks are tagged for all active VLANs.
- **Native VLAN:** Unused ports and Trunks use `VLAN 666` (Blackhole) as Native to prevent VLAN hopping.
- **Spanning Tree:** RSTP enabled globally.

### 3.3. Wireless Logic (MikroTik)
- **Mode:** Bridge AP with VLAN filtering.
- **SSID Mapping:** SSIDs are mapped to specific VLANs at the bridge ingress.
- **Management:** In-band management on VLAN 99.

## 4. Security & Wireless Decisions

### 4.1. Security Strategy
- **Zone-Based Firewalling:** Traffic is grouped into zones (LAN, Guest, Server, DMZ) to simplify policy management.
- **Implicit Deny:** The final rule in the policy set is always a DENY ALL.
- **Deep Dive:** See [04_security.md](04_security.md) for detailed firewall policies and logic.

### 4.2. Wireless Strategy
- **Frequency Planning:** 2.4GHz for legacy/IoT, 5GHz for high-speed clients.
- **Guest Access:** Isolated on VLAN 20 with no access to internal RFC1918 ranges.
- **Deep Dive:** See [06_wireless.md](06_wireless.md) for radio tuning and SSID details.
