from math import sin, cos, sqrt, atan2, radians, acos
import sys, traceback

# still have bug
def calculate_distance(lat1, lon1, lat2, lon2):
    return 0
    # approximate radius of earth in km
    R = 6373.0
    dlon = radians(lon2) - radians(lon1)
    dlat = radians(lat2) - radians(lat1)
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return round(distance, 3)

def add_station(row, stations):
    station_key = row['start station id']
    station_value = stations.get(station_key)
    if station_value is None:
        stations.update({station_key: (row['start station latitude'],
                                       row['start station longitude'],
                                       row['start station name'])})

def add_or_update_edge(row, edges):
    edge_key = (row['start station id'], row['end station id'])
    edge_value = edges.get(edge_key)
    # second to hour
    duration = row['tripduration']

    if edge_value is None:
        distance = calculate_distance(row['start station latitude'],
                                      row['start station longitude'],
                                      row['end station latitude'],
                                      row['end station longitude'])
        edge_value = {'duration': duration, 'count': 1, 'distance': distance}
    else:
        duration = edge_value.get('duration') + duration
        count = edge_value.get('count') + 1
        edge_value['duration'] = duration
        edge_value['count'] = count

    edges.update({edge_key: edge_value})
