# one minute looks like:
#   [{"192.168.1.1": 1000, "10.2.1.2": 234},
#    {"192.168.1.1": 90, "10.2.1.2": 234},
#
#     ...for 60 rows...
#
#    {...}]
# so this array gets updated by chopping the end and prepending the new minute

# Interface adapter set with first flag
import sys
ifadapter = sys.argv[1]

# Convert IP's to Hostnames
import socket

ips_to_hostnames = {}
def add_ips_to_hostnames(ips):
    for ip in ips.keys():
        if ip not in ips_to_hostnames:
            try:
                ips_to_hostnames[ip] = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                ips_to_hostnames[ip] = ip


# Graph Printing Code
import pandas as pd
import matplotlib.pyplot as plt

def print_graph(minute_byte_count):
    
    def format_packet_data(minute_byte_count):
        # Create labels for time intervals
        labeled_packets = zip(map(str, range(0, len(minute_byte_count))), minute_byte_count)

        # Format data
        address_throughputs = {}
        for timeslot, addresses in labeled_packets:
            for address, throughput in addresses.items():
                hostname = ips_to_hostnames[address]
                if hostname not in address_throughputs:
                    address_throughputs[hostname] = {}
                address_throughputs[hostname][timeslot] = throughput

        return address_throughputs

    # Set variables
    address_throughputs = format_packet_data(minute_byte_count)

    # Plot the data
    plt.close()
    df = pd.DataFrame(address_throughputs)
    df.plot.bar(stacked=True)
    plt.show(block=False)
    plt.pause(1)
    

# Packet Sniffing Code
from collections import Counter
from scapy.all import sniff

# Sum bytes sent in each second
sniff_data = {}
def sum_packet_lengths(packet):
    if packet[1].dst not in sniff_data:
        sniff_data[packet[1].dst] = len(packet)
    else:
        sniff_data[packet[1].dst] += len(packet)

## Setup sniff, filtering for IP traffic
minute_byte_count = []
for i in range(0, 10):

    sniff_data = {}
    sniff(iface=ifadapter, filter="ip", prn=sum_packet_lengths, timeout=1)

    add_ips_to_hostnames(sniff_data)

    if len(minute_byte_count) == 60:
        minute_byte_count = minute_byte_count[:-1]
    
    minute_byte_count.insert(0, sniff_data)
    
    print_graph(minute_byte_count)
