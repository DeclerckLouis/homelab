# SD-WAN Configuration

## 1. Overview
Software-Defined WAN (SD-WAN) is used to abstract the underlying WAN connectivity.  
Even with a single uplink, using the SD-WAN interface (`virtual-wan-link`) allows for easier policy management and future expansion (e.g., adding LTE failover).  

## 2. SD-WAN Members

| Interface | Alias | Status | Role |
| :--- | :--- | :--- | :--- |
| **wan** | ISP Uplink | Active | Primary Gateway |

## 3. SD-WAN Rules
Currently, the default implicit rule is in effect:  
- **Algorithm:** Source IP based load balancing (effectively single path with one member).  
- **Destination:** `0.0.0.0/0` redirects to `virtual-wan-link`.  

## 4. SLA Targets
*No specific SLA targets (Jitter/Packet Loss) configured at this time.*
