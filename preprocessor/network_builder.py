import pandas as pd
from preprocessor.network_builder_functions import NetworkBuilderFunctions


class NetworkBuilder:

    def __init__(self):
        path_to_data = "data/NYC-CitiBike-2016.csv"
        self.data_preprocessed = NetworkBuilderFunctions.preprocess_data(path_to_data)
        self.nodes = NetworkBuilderFunctions.get_nodes(self.data_preprocessed)
        self.edges = NetworkBuilderFunctions.get_edges(self.data_preprocessed)
        self.min_max_nodes = NetworkBuilderFunctions.get_min_max_node(self.nodes)
        self.network = NetworkBuilderFunctions.build(nodes=self.nodes, edges=self.edges)
