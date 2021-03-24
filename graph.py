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
    # Create labels for time intervals
    labeled_packets = dict(zip(map(str, range(0, len(timeslot_packets))), timeslot_packets))

    # Format data
    address_throughputs = {}
    for timeslot, addresses in labeled_packets.items():
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
