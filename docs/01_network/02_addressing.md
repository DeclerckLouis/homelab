# Network Addressing & VLANs

## 1. Overview
This document details the logical segmentation of the network, including VLAN assignments, IPv4 subnetting, and the IPv6 addressing strategy.

## 2. Network Segmentation & Addressing
The network follows a strict segmentation policy using hierarchical supernets and VLANs.

### 2.1. IPv4 Supernets
| Supernet | Name | Description |
| :--- | :--- | :--- |
| `10.0.0.0/8` | **PacketFlow** | Global Supernet |
| `10.10.0.0/16` | **Home Office** | Primary Site (Lab & Residence) |
| `10.20.0.0/16` | **Branch Office** | Remote Site |

### 2.2. VLANs & Subnets
| VLAN ID | Name | IPv4 Subnet | IPv6 Subnet | Key Addresses / Notes | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **10** | `Home` | `10.10.10.0/24` | `fdb1:6575:ad8a:10::/64` | GW: `10.10.10.1` | **Default Trusted Network.** "Office" devices. |
| **20** | `Guest` | `10.10.20.0/24` | `fdb1:6575:ad8a:20::/64` | GW: `10.10.20.1` | **Guest Network.** Personal devices and WiFi - Isolated. |
| **30** | `Servers` | `10.10.30.0/24` | `fdb1:6575:ad8a:30::/64` | GW: `10.10.30.1` | **Servers.** Docker, VMs, Raspberry Pis. |
| **33** | `Device Prep` | `10.10.33.0/24` | `fdb1:6575:ad8a:33::/64` | GW: `10.10.33.1` | **Staging.** For preparing new devices. (not used) |
| **35** | `DMZ` | `10.10.35.0/24` | `fdb1:6575:ad8a:35::/64` | GW: `10.10.35.1` | **DMZ.** Public facing services. |
| **99** | `MGMT` | `10.10.99.0/24` | `fdb1:6575:ad8a:99::/64` | GW4: `10.10.99.1`<br>GW6: `FE80::99:1/64` | **Management.** Infrastructure management. |
| **666** | `Blackhole`| N/A | N/A | Isolated | **Dead VLAN.** Native VLAN security. |

### 2.3. Notes
- **IPv6 Strategy**: Uses Unique Local Addresses (ULA) `fdb1:6575:ad8a::/48` for internal stability.
- **Servers**: Currently running Grafana and Netbox (VLAN 30). Future: HAProxy (DMZ).
- **Future**: IoT VLAN (VLAN 31) planned for printers and IoT devices.

## 3. Configuration Details

<details>
<summary><b>VLAN 10 (Home)</b></summary>

```bash
config system interface
    edit "VLAN10"
        set vdom "root"
        set ip 10.10.10.1 255.255.255.0
        set allowaccess ping
        set alias "VLAN Default"
        set device-identification enable
        set role lan
        set snmp-index 12
        set ip-managed-by-fortiipam disable
        config ipv6
            set ip6-address fdb1:6575:ad8a:10::1/64
            set ip6-allowaccess ping
            config ip6-extra-addr
                edit fe80::10:1/64
                next
            end
            set ip6-send-adv enable
            set ip6-other-flag enable
            config ip6-prefix-list
                edit fdb1:6575:ad8a:10::/64
                next
            end
        end
        set interface "mgmt"
        set vlanid 10
    next
end
```
</details>

<details>
<summary><b>VLAN 20 (Guest)</b></summary>

```bash
config system interface
    edit "VLAN20"
        set vdom "root"
        set ip 10.10.20.1 255.255.255.0
        set allowaccess ping
        set alias "VLAN Guest"
        set device-identification enable
        set role lan
        set snmp-index 13
        set ip-managed-by-fortiipam disable
        config ipv6
            set autoconf enable
        end
        set interface "mgmt"
        set vlanid 20
    next
end
```
</details>

<details>
<summary><b>VLAN 30 (Servers)</b></summary>

```bash
config system interface
    edit "VLAN30"
        set vdom "root"
        set ip 10.10.30.1 255.255.255.0
        set allowaccess ping
        set alias "VLAN Servers"
        set device-identification enable
        set role lan
        set snmp-index 14
        set ip-managed-by-fortiipam disable
        config ipv6
            set ip6-address fdb1:6575:ad8a:30::1/64
            set ip6-allowaccess ping
            config ip6-extra-addr
                edit fe80::30:1/64
                next
            end
            set ip6-send-adv enable
            set ip6-other-flag enable
            config ip6-prefix-list
                edit fdb1:6575:ad8a:30::/64
                next
            end
        end
        set interface "mgmt"
        set vlanid 30
    next
end
```
</details>

<details>
<summary><b>VLAN 33 (Device Prep)</b></summary>

```bash
config system interface
    edit "VLAN 33"
        set vdom "root"
        set ip 10.10.33.1 255.255.255.0
        set allowaccess ping fabric speed-test
        set alias "VLAN Device Prep"
        set device-identification enable
        set role lan
        set snmp-index 18
        set ip-managed-by-fortiipam disable
        config ipv6
            set ip6-address fdb1:6575:ad8a:33::1/64
            set ip6-allowaccess ping
            config ip6-extra-addr
                edit fe80::33:1/64
                next
            end
            set ip6-send-adv enable
            set ip6-other-flag enable
            config ip6-prefix-list
                edit fdb1:6575:ad8a:33::/64
                next
            end
        end
        set interface "mgmt"
        set vlanid 33
    next
end
```
</details>

<details>
<summary><b>VLAN 35 (DMZ)</b></summary>

```bash
config system interface
    edit "VLAN35"
        set vdom "root"
        set ip 10.10.35.1 255.255.255.0
        set alias "VLAN DMZ"
        set device-identification enable
        set role dmz
        set snmp-index 15
        set ip-managed-by-fortiipam disable
        config ipv6
            set ip6-address fdb1:6575:ad8a:35::1/64
            set ip6-allowaccess ping
            config ip6-extra-addr
                edit fe80::35:1/64
                next
            end
            set ip6-send-adv enable
            set ip6-other-flag enable
            config ip6-prefix-list
                edit fdb1:6575:ad8a:35::/64
                next
            end
        end
        set interface "mgmt"
        set vlanid 35
    next
end
```
</details>

<details>
<summary><b>VLAN 99 (Management)</b></summary>
> [!NOTE]
> Note the `ip6-extra-addr` configuration which assigns the manual Link-Local address `fe80::99:1/64` for easy management access.

```bash
config system interface
    edit "VLAN10"
        set vdom "root"
        set ip 10.10.10.1 255.255.255.0
        set allowaccess ping
        set alias "VLAN Default"
        set device-identification enable
        set role lan
        set snmp-index 12
        set ip-managed-by-fortiipam disable
        config ipv6
            set ip6-address fdb1:6575:ad8a:10::1/64
            set ip6-allowaccess ping
            config ip6-extra-addr
                edit fe80::10:1/64
                next
            end
            set ip6-send-adv enable
            set ip6-other-flag enable
            config ip6-prefix-list
                edit fdb1:6575:ad8a:10::/64
                next
            end
        end
        set interface "mgmt"
        set vlanid 10
    next
end
```
</details>

<details>
<summary><b>Blackhole (VLAN 666)</b></summary>

```bash
config system interface
    edit "Blackhole"
        set vdom "root"
        set alias "VLAN Blackhole"
        set device-identification enable
        set role lan
        set snmp-index 16
        set ip-managed-by-fortiipam disable
        set interface "mgmt"
        set vlanid 666
    next
end
```
</details>
