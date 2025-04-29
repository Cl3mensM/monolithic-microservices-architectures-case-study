import osmnx as ox
import pandas as pd
import geopandas as gpd
import os
from routing.models import Disruption

PLACE = "Innere Stadt, Vienna, Austria"
FILE_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_from_map_data(filename):
    """Load a file from the map_data folder."""
    return os.path.join(FILE_BASE_DIR, "map_data", filename)


def get_graph():
    # G = ox.graph.graph_from_place(PLACE, network_type="walk")
    graph_path = os.path.join(
        FILE_BASE_DIR, "map_data", "innere_stadt.graphml")
    G = ox.load_graphml(graph_path)
    return G


def get_bus_stops():
    # bus = ox.features.features_from_place(PLACE, tags={"highway": "bus_stop"})
    return gpd.read_file(load_from_map_data("bus_stops.geojson"))


def get_subway_stops():
    # subway = ox.features.features_from_place(
    #     PLACE, tags={"railway": "station", "station": "subway"})
    return gpd.read_file(load_from_map_data("subway_stops.geojson"))


def get_tram_stops():
    # tram = ox.features.features_from_place(
    #     PLACE, tags={"railway": "tram_stop"})
    return gpd.read_file(load_from_map_data("tram_stops.geojson"))


def calculate_route(start, end, G):
    start_node = ox.distance.nearest_nodes(G, start[0], start[1])
    end_node = ox.distance.nearest_nodes(G, end[0], end[1])
    route = ox.routing.shortest_path(G, start_node, end_node)
    return route


def calculate_routes_same_start(start, ends, G):
    routes = []
    for end in ends:
        route = calculate_route(start, end, G)
        routes.append(route)
    return routes


def get_shortest_route(routes, G):
    route, route_length = None, float("inf")
    for r in routes:
        edge_lengths = ox.routing.route_to_gdf(G, r)["length"]
        r_length = sum(edge_lengths)
        if r_length < route_length:
            route, route_length = r, r_length
    return route


def route_for_user_request(latitude, longitude, bus, tram, subway):
    G = get_graph()
    all_stops, stops_coordinates = get_all_stops(bus, tram, subway)

    all_stops, stops_coordinates = filter_disrupted_stations(
        all_stops, stops_coordinates)

    start = (longitude, latitude)
    routes = calculate_routes_same_start(start, stops_coordinates, G)
    route = get_shortest_route(routes, G)
    index = routes.index(route)
    stop = all_stops.iloc[index]
    return route, stop


def extract_coordinates_from_stops(stops):
    return [(stops.geometry.x.iloc[i], stops.geometry.y.iloc[i]) for i in range(len(stops))]


def get_current_disruptions():
    return Disruption.objects.all()


def get_all_stops(bus, tram, subway):
    """Fetch all stops and their coordinates based on transport types."""
    stops_coordinates = []
    all_stops = pd.DataFrame()

    if bus:
        bus_stops = get_bus_stops()
        stops_coordinates.extend(extract_coordinates_from_stops(bus_stops))
        all_stops = pd.concat([all_stops, bus_stops], ignore_index=True)

    if tram:
        tram_stops = get_tram_stops()
        stops_coordinates.extend(extract_coordinates_from_stops(tram_stops))
        all_stops = pd.concat([all_stops, tram_stops], ignore_index=True)

    if subway:
        subway_stops = get_subway_stops()
        stops_coordinates.extend(extract_coordinates_from_stops(subway_stops))
        all_stops = pd.concat([all_stops, subway_stops], ignore_index=True)

    return all_stops, stops_coordinates


def filter_disrupted_stations(all_stops, stops_coordinates):
    """Filter out stations with disruptions."""
    disruptions = get_current_disruptions()
    station_name_disruptions = [
        disruption.station_name for disruption in disruptions]

    indices_to_remove = [
        i for i in range(len(all_stops)) if all_stops.iloc[i]["name"] in station_name_disruptions
    ]

    all_stops.drop(indices_to_remove, inplace=True)
    stops_coordinates = [
        coord for idx, coord in enumerate(stops_coordinates) if idx not in indices_to_remove
    ]

    all_stops.reset_index(drop=True, inplace=True)

    return all_stops, stops_coordinates
