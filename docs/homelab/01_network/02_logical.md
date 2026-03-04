# Logical layout

## 1. Business drivers and goals
The **Packetflow Homelab** network typically serves two primary functions:
1.  **Production Home Network:** Providing stable, high-speed internet access for daily use (working from home, streaming, gaming).
2.  **Experimental Lab:** A playground for learning networking concepts (IPv6, BGP, SD-WAN, segmentation).

**Key Goals:**
- **Strict Segmentation:** Isolating "Home" traffic from "Guest" and "Server" traffic.
- **IPv6 First:** Implementing a dual-stack network with a focus on IPv6.
- **Vendor Diversity:** Gaining proficiency with Fortinet, Ubiquiti, and MikroTik ecosystems.

## 2. Global Network Design
The network architecture is designed to support a multi-site topology, although currently only the primary site is active.

- **Home Office (HQ):** The primary site hosting the core infrastructure (`10.10.0.0/16`).
- **Branch Office (Remote):** A planned remote site for simulating site-to-site VPNs (`10.20.0.0/16`).
- **Cloud/VPS:** External resources connected via VPN (for example, VPS for off-site backups/monitoring).

## 3. Naming conventions
Use a consistent naming convention to identify devices and interfaces easily.

**Format:** `[ROLE][INDEX].[DOMAIN]`

- **Roles:**
    - `FW`: Firewall / Router (for example, `FW01`)
    - `ALS`: Access Layer Switch (for example, `ALS01`)
    - `DLS`: Distribution Layer Switch (for example, `DLS01`)
    - `AP`: Access Point (for example, `AP01`)
    - `SRV`: Server (for example, `SRV01`)
- **Domain:** `lab.internal.packetflow.be`

**Interface Naming:**
- **VLANs:** `VLAN[ID]` (for example, `VLAN10`)
- **L3 Interfaces:** Interactive names (for example, `wan`, `lan`, `dmz`)

## 4. Logical topology
*(Layer 2 and Layer 3 diagrams showing VLANs, Trunks, and Routing paths)*

**[Image Placeholder: Logical Topology Diagram]**

## 5. IP addressing scheme

### 5.1. Supernets
| Supernet       | Name              | Description                    |
| :------------- | :---------------- | :----------------------------- |
| `10.0.0.0/8`   | **PacketFlow**    | Global Supernet                |
| `10.10.0.0/16` | **Home Office**   | Primary Site (Lab & Residence) |
| `10.20.0.0/16` | **Branch Office** | Remote Site                    |

### 5.2. VLANs and subnets
| VLAN ID | Name        | IPv4 Subnet     | IPv6 Subnet (ULA)        | Gateway | Description                                             |
| :------ | :---------- | :-------------- | :----------------------- | :------ | :------------------------------------------------------ |
| **10**  | `Home`      | `10.10.10.0/24` | `fdb1:6575:ad8a:10::/64` | `.1`    | **Default Trusted Network.** "Office" devices.          |
| **20**  | `Guest`     | `10.10.20.0/24` | `fdb1:6575:ad8a:20::/64` | `.1`    | **Guest Network.** Isolated Internet access only.       |
| **30**  | `Servers`   | `10.10.30.0/24` | `fdb1:6575:ad8a:30::/64` | `.1`    | **Servers.** Docker, VMs, Pis.                          |
| **35**  | `DMZ`       | `10.10.35.0/24` | `fdb1:6575:ad8a:35::/64` | `.1`    | **DMZ.** Public facing services (for example, HAProxy). |
| **99**  | `MGMT`      | `10.10.99.0/24` | `fdb1:6575:ad8a:99::/64` | `.1`    | **Management.** Network device management.              |
| **666** | `Blackhole` | N/A             | N/A                      | N/A     | **Dead VLAN.** Used for Native VLAN security.           |

*Note: IPv6 Local Link addresses for Gateways are manually set to `fe80::[VLAN_ID]:1` for consistency.*

## 6. Routing and WAN

### 6.1. Routing protocols
- **IGP:** Currently using **Connected** and **Static** routing. OSPF/BGP planned for future Branch Office integration.
- **Default Route:** `0.0.0.0/0` pointed to ISP Gateway via PPPoE/DHCP.

### 6.2. SD-WAN
- **Interface:** `virtual-wan-link`
- **Members:** `wan1` (ISP Uplink)
- **Strategy:** Even with a single uplink, SD-WAN abstracts policies.
- **Rules:**
    - Source IP load balancing (default).
    - `0.0.0.0/0` -> `virtual-wan-link`.

### 6.3. Inter-VLAN routing
- Performed by **FortiGate 40F**.
- **Policy:** Default Deny. Traffic must be explicitly allowed via Firewall Policies.
