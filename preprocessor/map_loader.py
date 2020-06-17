import geopandas as gpd


class MapLoader:
    def __init__(self):
        path_to_data = "nybb"
        data_raw = gpd.read_file(gpd.datasets.get_path(path_to_data))

        # convert coordinates to epsg:3857
        self.data = data_raw.to_crs(epsg=3857)


