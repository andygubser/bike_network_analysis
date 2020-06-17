from preprocessor.network_loader import NetworkLoader
from preprocessor.map_loader import MapLoader
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import networkx as nx


# load network data
network_loader = NetworkLoader()
nodes, edges = network_loader.nodes, network_loader.edges


map_loader = MapLoader()
geodata_nyc = map_loader.data_processed

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# visualize the network
fig, ax = plt.subplots(figsize=(30, 30))
plot_nyc = geodata_nyc.plot(alpha=0.5, edgecolor="k", ax=ax)
ctx.add_basemap(plot_nyc)
nx.draw_networkx(G, ax=ax, pos=nodes)

plt.xlim((xmin, xmax))
plt.ylim((ymin, ymax))
plt.show()
