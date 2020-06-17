import pandas as pd
from preprocessor.network_functions import NetworkFunctions


class NetworkLoader:

    def __init__(self):
        path_to_data = "data/NYC-CitiBike-2016.csv"
        self.data_preprocessed = NetworkFunctions.preprocess_data(path_to_data)
        self.nodes = NetworkFunctions.get_nodes(self.data_preprocessed)
        self.edges = NetworkFunctions.get_edges(self.data_preprocessed)
        self.min_max_nodes = NetworkFunctions.get_min_max_node(self.nodes)




# network_data_loader = NetworkDataLoader()
# network_data_loader.nodes
# network_data_loader.edges


