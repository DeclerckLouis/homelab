# Physical layout

## 1. Sites
To standardize network deployments, sites are categorized and documented based on their function and requirements.

| Name                        | Description                                                     | Requirements                                             |
| :-------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------- |
| **(default) Home Office**   | Primary residence and main lab environment.                     | High availability, 10GbE core, experimental hardware.    |
| **(default) Branch Office** | Remote locations (for example, family homes connected via VPN). | Low maintenance, stable connectivity, remote management. |
| **Guest**                   | Roaming devices connecting via VPN.                             | Secure access to internal resources.                     |

## 2. Hardware inventory (BOM)
Current hardware deployed in the **Home Office** site.

| Device Role           | Make / Model              | Hostname  | Description / Notes                                                 |
| :-------------------- | :------------------------ | :-------- | :------------------------------------------------------------------ |
| **Router / Firewall** | Fortinet FortiGate 40F    | `FW01`    | Main internet gateway and security appliance.                       |
| **Core Switch**       | Ubiquiti EdgeSwitch 8 PoE | `ALS01`   | Managed L2 switch providing PoE to APs and connectivity to servers. |
| **Access Point**      | MikroTik hAP ac lite      | `AP01`    | Dual-concurrent Access Point. Used to learn MikroTik RouterOS.      |
| **Compute**           | Generic Servers           | *Various* | Hypervisors and storage servers.                                    |

*Note: All hosts are part of the `lab.internal.packetflow.be` domain.*

## 3. Physical topology
The network centers around a "Core Rack" configuration where the FortiGate handles WAN and the EdgeSwitch handles internal distribution.

**[Image Placeholder: Physical Topology Diagram]**
*(Include rack diagram here)*

## 4. Cabling and port map

### FortiGate 40F (`FW01`)
| Port | Type | Connected Device | Notes                                |
| :--- | :--- | :--------------- | :----------------------------------- |
| WAN  | RJ45 | ISP Modem        | Public IP via DHCP/PPPoE             |
| 1    | RJ45 | AP01             | HAP AC Lite currently used as AP     |
| 2    | RJ45 | ALS01            | Main Trunk Link (Carries all VLANs)  |
| 3    | RJ45 | *Reserved*       | Emergency Management / Direct Access |

### Ubiquiti EdgeSwitch 8 PoE (`ALS01`)
| Port | Profile      | Connected Device   | PoE Mode    |
| :--- | :----------- | :----------------- | :---------- |
| 1    | Trunk        | **uplink to FW01** | POE+ (0W)   |
| 2-8  | Access/Trunk | Servers / IoT      | *As needed* |

### MikroTik hAP ac lite (`AP01`)

*Radio configuration:*
- **wlan1 (2.4GHz):** Legacy/IoT devices  
- **wlan2 (5GHz):** High-speed clients  

!!! note "Note"
    This device currently serves the home WiFi. This is done to generate some real traffic on the network.  
    While not necessarily best practice, it allows you to spot issues faster.