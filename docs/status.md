# System status and incident log

**Current Status:**   
:white_check_mark: **No outages**
!!! note "This is currently manually updated."

---
## Incident history

### 2026

#### February 10, 2026 - IPv4 connectivity loss

!!! warning "Outage: Partial internet loss"
    - **Time:** 04:00 - 15:15 CET
    - **Issue**  
        fw01 failed to acquire a WAN IPv4 address from the ISP modem.  
        Local network devices lost access to IPv4 internet services.  
        Local IPv6 and IPv4 traffic remained operational.  
    - **Impact**  
        - **Users:** Medium. Most client devices automatically switched to the Telenet modem WiFi.
        - **Services:** No services connected, all LAN traffic  
        - **Unaffected:** Local LAN traffic and IPv6-enabled sites (Google/YouTube).  
    - **Root cause**  
        The ISP modem DHCP service hung or entered a stale state, refusing to renew the lease for the firewall's WAN interface.  
    - **Resolution**  
        Physical power cycle of the ISP modem. Connectivity was restored immediately upon reboot.  