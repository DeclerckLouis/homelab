# Routing & Switching

## 1. Overview
This document covers the Layer 2 (Data Link) and Layer 3 (Network) forwarding logic.  
The network uses **Fortinet** for L3 routing/firewalling and **Ubiquiti/MikroTik** for L2 switching and wireless bridging.

## 2. Layer 2: Switching Logic

### 2.1. Ubiquiti EdgeSwitch (Core)
The EdgeSwitch acts as the central L2 distribution point.

- **VLANs:** 10, 20, 30, 35, 99 defined database.
- **Trunk Ports:** Tagged traffic for all active VLANs. 
  - **Native VLAN:** Set to **666 (Blackhole)** on uplinks to prevent VLAN hopping attacks.
- **Access Ports:** Untagged for specific VLANs (e.g., Server links).
- **Spanning Tree:** RSTP enabled to prevent loops.

### 2.2. MikroTik (Access)
The MikroTik `hAP ac lite` uses **Bridge VLAN Filtering**.

- **Bridge:** Single `bridgeLocal` with `vlan-filtering=yes`.
- **Hybrid Ports:** 
  - `ether1` (Uplink): Tagged for VLANs 10, 20, 99. Native/PVID 666 (Dummy matching Blackhole).
  - WiFi Interfaces: PVID set dynamically or via Bridge Port PVID to drop clients into VLAN 20 (Office) or 10 (Home).

## 3. Layer 3: Routing Logic

### 3.1. General Routing (IPv4)
- **Gateway:** FortiGate 40F (`10.x.x.1` on all subnets).
- **Inter-VLAN Routing:** Performed by FortiGate. Default DENY. strict firewall policies required to allow traffic.
- **Default Route:** `0.0.0.0/0` via WAN interface (DHCP/PPPoE from ISP).

### 3.2. IPv6 Routing
- **Method:** **Router Advertisements (RA)** with SLAAC/DHCPv6.
- **ULA Advertisement:** 
  - The FortiGate is configured to advertise the ULA prefix `fdb1:6575:ad8a::/48` on each interface.
  - **Flags:** `Managed (M)` flag OFF, `Other (O)` flag ON (Stateless DHCPv6 for DNS).
  - Use `radvd` or FortiOS `config ipv6` settings to ensure the 'A' (Autonomous) flag is set so clients auto-configure addresses.

### 3.3. SD-WAN (Brief)
SD-WAN is enabled to manage traffic prioritization, though currently primarily functioning with a single WAN link for policy abstraction. (See `05_sd_wan.md` for details).
