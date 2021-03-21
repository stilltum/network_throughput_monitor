import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# one minute looks like:
#   [{"192.168.1.1": 1000, "10.2.1.2": 234},
#    {"192.168.1.1": 90, "10.2.1.2": 234},
#
#     ...for 60 rows...
#
#    {...}]
# so this array gets updated by chopping the end and prepending the new minute
def get_graph_height(outgoing_packets):
    graph_height = 0.0
    for packet in outgoing_packets:
        hits = 0.0
        for hit in packet.values():
            hits += hit
        if hits > graph_height:
            graph_height = hits

    return graph_height

def get_percentages(all_addresses, timeslot_packets, height):
    packet_percentages = {}
    timeslot = 0
    for timeslot_ip in timeslot_packets:
        for address in all_addresses:
            if str(timeslot) not in packet_percentages:
                packet_percentages[str(timeslot)] = {}

            if address in timeslot_ip:
                packet_percentages[str(timeslot)][address] = timeslot_ip[address] / height
            else:
                packet_percentages[str(timeslot)][address] = 0
        timeslot += 1

    return packet_percentages

# Set variables
timeslot_packets = [{"192.168.1.1": 1000, "10.2.1.2": 234, "1.1.1.1": 111}, {"192.168.1.1": 90, "10.2.1.2": 234}]
graph_height = get_graph_height(timeslot_packets)

# get all addresses
all_addresses = set()
timeslot_addresses = list(map(lambda packet: [*packet], timeslot_packets))
for timeslot in timeslot_addresses:
    for address in timeslot:
        all_addresses.add(address)
all_addresses = [*all_addresses]

graph_percentages = get_percentages(all_addresses, timeslot_packets, graph_height)

# Format the data
address_throughput = {}
for timeslot, addresses in graph_percentages.items():
    for address, throughput in addresses.items():
        if address not in address_throughput:
            address_throughput[address] = {}
        address_throughput[address][timeslot] = throughput

# Plot the data
df = pd.DataFrame(address_throughput)
df.plot.bar(stacked=True)

plt.show()
