# from scapy.all import *

# eth = Ether(src="00:00:00:00:00:03", dst="00:00:00:00:00:22", type=0x0800)  
# ip = IP(src="192.168.20.1" , dst="192.168.10.1", proto=0x06)
# tcp = TCP(sport=1234, dport=80, flags="S")

# pkt = eth/ip/tcp
# # Send the packet
# sendp(pkt, iface="enp7s0np0")

# eth = Ether(src="00:00:00:00:00:03", dst="00:00:00:00:00:22", type=0x0800)  
# ip = IP(src="192.168.20.1" , dst="192.168.10.1", proto=0x06)
# tcp = TCP(sport=1234, dport=80, flags="")

# pkt = eth/ip/tcp
# # Send the packet
# sendp(pkt, iface="enp7s0np0")

from scapy.all import *

eth = Ether(src="00:00:00:00:00:03", dst="00:00:00:00:00:22", type=0x0800)
ip = IP(src="192.168.20.1", dst="192.168.10.1", proto=0x11)
udp = UDP(sport=1234, dport=80)

pkt = eth/ip/udp

sendp(pkt, iface="enp7s0np0")

