import pandas as pd
import networkx as nx
from pyproj import CRS, Transformer


class NetworkBuilderFunctions:

    # data preprocessor
    @classmethod
    def preprocess_data(cls, path_to_data):
        df_raw = cls._read_data(path_to_data)
        df_renamed = cls._rename_columns(df_raw)
        df_cleaned = cls._drop_unknown_lat_long(df_renamed)
        return df_cleaned

    @staticmethod
    def _read_data(path_to_data):
        return pd.read_csv(path_to_data)

    @staticmethod
    def _rename_columns(df):
        df.columns = df.columns.str.replace(" ", "_")
        return df

    @staticmethod
    def _drop_unknown_lat_long(df):
        return df[(df["start_station_latitude"] != 0) &
                  (df["start_station_longitude"] != 0) &
                  (df["end_station_latitude"] != 0) &
                  (df["end_station_longitude"] != 0)]

    # get nodes
    @classmethod
    def get_nodes(cls, df):
        stations_unique = cls._get_unique_stations(df)
        stations_corrected_coord = cls._transform_coordinates(stations_unique)
        stations_dict = cls._create_dict(stations_corrected_coord)
        return stations_dict

    @staticmethod
    def _get_unique_stations(df):
        start_station_coord = df[["start_station_id",
                                  "start_station_name",
                                  "start_station_latitude",
                                  "start_station_longitude"]]. \
            drop_duplicates(). \
            rename(columns={"start_station_id": "id",
                            "start_station_name": "name",
                            "start_station_latitude": "lat",
                            "start_station_longitude": "long"})

        end_station_coord = df[["end_station_id",
                                "end_station_name",
                                "end_station_latitude",
                                "end_station_longitude"]]. \
            drop_duplicates(). \
            rename(columns={"end_station_id": "id",
                            "end_station_name": "name",
                            "end_station_latitude": "lat",
                            "end_station_longitude": "long"})

        stations = pd.concat([start_station_coord, end_station_coord]). \
            drop_duplicates(subset="id"). \
            sort_values("id"). \
            set_index("id")
        return stations

    @classmethod
    def _transform_coordinates(cls, df):
        df[["lat_transformed", "long_transformed"]] = \
            df[["lat", "long"]].apply(cls._convert_coordinates, axis=1)

        # reverse lat - long
        df[["lat_transformed", "long_transformed"]] = df[["long_transformed", "lat_transformed"]]
        return df

    @staticmethod
    def _convert_coordinates(row):
        """
        transform coordinates from epsg:4326 (GPS lat, long) to epsg:3857 (Mapping Aplications)
        :param row:
        :return:
        """
        crs_input = CRS("EPSG:4326")
        crs_output = CRS("EPSG:3857")
        transformer = Transformer.from_crs(crs_from=crs_input, crs_to=crs_output)

        # in_proj = pyproj.Proj(init='epsg:4326')
        # out_proj = pyproj.Proj(init='epsg:3857')
        lat_transformed, long_transformed = \
            transformer.transform(row["lat"], row["long"])
        return pd.Series({"lat_transformed": long_transformed, "long_transformed": lat_transformed})

    @staticmethod
    def _create_dict(df):
        df["pos"] = list(zip(df["lat_transformed"], df["long_transformed"]))
        return df["pos"].drop_duplicates().to_dict()

    @classmethod
    def get_edges(cls, df):
        return list(zip(df["start_station_id"], df["end_station_id"]))

    @classmethod
    def get_min_max_node(cls, nodes):
        nodes_df = pd.DataFrame(nodes).T
        xmin = nodes_df.min()[0]
        ymin = nodes_df.min()[1]
        xmax = nodes_df.max()[0]
        ymax = nodes_df.max()[1]
        return xmin, xmax, ymin, ymax

    @classmethod
    def build(cls, nodes, edges):
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G




