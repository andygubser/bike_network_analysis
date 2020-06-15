import networkx as nx
import pandas as pd
import bike_utils

df = pd.read_csv("./data/NYC-CitiBike-2016.csv")
df.head()

edges = dict()
stations = dict()

# run about 30 seconds
for index, row in df.iterrows():
    bike_utils.add_station(row, stations)
    bike_utils.add_or_update_edge(row, edges)

len(edges)
len(stations)

list(edges.keys())[1]
list(edges.values())[1]

DG = nx.DiGraph()
for key, value in edges.items():
    DG.add_edges_from([(*key, {'weight': value['count'],
                               'duration': round(value['duration'] / 60),
                               'distance': value['distance']})])

for key, value in stations.items():
    DG.nodes[key]['lat'] = value[0]
    DG.nodes[key]['lon'] = value[1]
    DG.nodes[key]['name'] = value[2]

# node
DG.nodes[3178]
# edge
DG[3164][3178]