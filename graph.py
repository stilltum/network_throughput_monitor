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
def format_packet_data(timeslot_packets):
    # Get all addresses across the time window
    all_addresses = set()
    timeslot_addresses = list(map(lambda packet: [*packet], timeslot_packets))
    for timeslot in timeslot_addresses:
        for address in timeslot:
            all_addresses.add(address)
    all_addresses = [*all_addresses]

    # Zero out columns that don't exist
    packet_heights = {}
    timeslot = 0
    print(timeslot_packets)
    for timeslot_ip in timeslot_packets:
        for address in all_addresses:
            if str(timeslot) not in packet_heights:
                packet_heights[str(timeslot)] = {}

            if address in timeslot_ip:
                packet_heights[str(timeslot)][address] = timeslot_ip[address]

        timeslot += 1

    # Format data
    address_throughputs = {}
    for timeslot, addresses in packet_heights.items():
        for address, throughput in addresses.items():
            if address not in address_throughputs:
                address_throughputs[address] = {}
            address_throughputs[address][timeslot] = throughput

    return address_throughputs

# Set variables
timeslot_packets = [{"192.168.1.1": 1000, "10.2.1.2": 234, "1.1.1.1": 111}, {"192.168.1.1": 90, "10.2.1.2": 234, "10.2.1.3": 100}]
address_throughputs = format_packet_data(timeslot_packets)

# Plot the data
df = pd.DataFrame(address_throughputs)
df.plot.bar(stacked=True)

plt.show()
