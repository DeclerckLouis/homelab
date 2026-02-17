# Physical Layout

## 1. Site Tiers
To standardize network deployments, sites are categorized into tiers based on their function and requirements.

| Tier | Description | Requirements |
| :--- | :--- | :--- |
| **Home Office** | Primary residence and main lab environment. | High availability, 10GbE core, experimental hardware. |
| **Branch Office** | Remote locations (e.g., family homes connected via VPN). | Low maintenance, stable connectivity, remote management. |
| **Mobile** | Roaming devices connecting via VPN. | Secure access to internal resources. |

## 2. Hardware Inventory (BOM)
Current hardware deployed in the **Home Office** tier.

| Device Role | Make / Model | Hostname | Description / Notes |
| :--- | :--- | :--- | :--- |
| **Router / Firewall** | Fortinet FortiGate 40F | `FW01` | Main internet gateway and security appliance. |
| **Core Switch** | Ubiquiti EdgeSwitch 8 PoE | `ALS01` | Managed L2 switch providing PoE to APs and connectivity to servers. |
| **Access Point** | MikroTik hAP ac lite | `AP01` | Dual-concurrent Access Point. **Used for learning MikroTik RouterOS.** |
| **Compute** | Generic Servers | *Various* | Hypervisors and storage servers. |

*Note: All hosts are part of the `lab.internal.packetflow.be` domain.*

## 3. Physical Topology
The network centers around a "Core Rack" configuration where the FortiGate handles WAN and the EdgeSwitch handles internal distribution.

**[Image Placeholder: Physical Topology Diagram]**
*(Include rack diagram here)*

## 4. Cabling & Port Map

### FortiGate 40F (`FW01`)
| Port | Type | Connected Device | Notes |
| :--- | :--- | :--- | :--- |
| WAN | RJ45 | ISP Modem | Public IP via DHCP/PPPoE |
| 1 | RJ45 | AP01 | HAP AC Lite currently used as AP |
| 2 | RJ45 | ALS01 | Main Trunk Link (Carries all VLANs) |
| 3 | RJ45 | *Reserved* | Emergency Management / Direct Access |

### Ubiquiti EdgeSwitch 8 PoE (`ALS01`)
| Port | Profile | Connected Device | PoE Mode |
| :--- | :--- | :--- | :--- |
| 1 | Trunk | **uplink to FW01** | POE+ (0W) |
| 2-8 | Access/Trunk | Servers / IoT | *As needed* |

### MikroTik hAP ac lite (`AP01`)
*Radio Configuration:*
- **wlan1 (2.4GHz):** Legacy/IoT devices
- **wlan2 (5GHz):** High-speed clients
