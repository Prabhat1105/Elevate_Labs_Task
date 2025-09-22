To begin the network analysis, I installed two essential tools: 
Nmap for active scanning and Wireshark for packet inspection.
Initial Packet Monitoring with Wireshark Before initiating any scans, I launched Wireshark to monitor live network traffic. 
I specifically filtered for TCP SYN packets, which are used during the initial handshake of a TCP connection. 
This helped identify potential connection attempts and gave insight into active hosts and services on the network.
Active Scanning with Nmap After observing the preliminary traffic, I used Nmap to perform a targeted scan on the desired IP address. This revealed a list of open ports and the services running on each port, allowing me to map the network footprint and identify accessible endpoints.
