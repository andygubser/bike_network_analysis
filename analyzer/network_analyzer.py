from preprocessor.network_builder import NetworkBuilder
from preprocessor.map_builder import MapBuilder
from

import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import networkx as nx


class NetworkAnalyser:
    def __init__(self):
        network_loader = NetworkBuilder()
        nodes, edges = network_loader.nodes, network_loader.edges


map_loader = MapBuilder()
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
