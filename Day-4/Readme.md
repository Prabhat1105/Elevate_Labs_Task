This project demonstrates configuring and testing basic firewall rules on Linux using UFW (Uncomplicated Firewall). 
The steps include checking the current firewall status, enabling UFW, setting default policies to deny incoming and allow outgoing traffic
Allowing SSH on port 22 to maintain remote access, and blocking Telnet on port 23 for security reasons.
After applying the rules, the configuration was verified using ufw status numbered, and connectivity to port 23 was tested using telnet.
Finally, the Telnet rule was removed, and the firewall state was restored. Screenshots of each step are included in the repository
