# System Status & Incident Log

**Current Status:**   
:white_check_mark: **No outages**
!!! Note "This is currently manually updated."

---
## Incident History
### 2026
#### February 10, 2026 - IPv4 Connectivity Loss
!!! warning "Outage: Partial Internet Loss"
    - **Time:** 04:00 - 15:15 CET
    - **Issue**  
        fw01 failed to acquire a WAN IPv4 address from the ISP modem.  
        Local network devices lost access to IPv4 internet services.  
        Local IPv6 and IPv4 traffic remained operational.  
    - **Impact**  
        -  **Users:** Medium. Most client devices automatically switched to the telenet modem wifi.
        - **Services:** No services connected, all LAN traffic 
        - **Unaffected:** Local LAN traffic and IPv6-enabled sites (Google/YouTube).  
    - **Root Cause**  
        The ISP Modem DHCP service hung or entered a stale state, refusing to renew the lease for the firewall's WAN interface.  
    - **Resolution**  
        Physical power cycle of the ISP Modem. Connectivity restored immediately upon reboot.  