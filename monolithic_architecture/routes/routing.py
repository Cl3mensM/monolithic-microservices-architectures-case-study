import osmnx as ox

PLACE = "Innere Stadt, Vienna, Austria"


def get_graph():
    G = ox.graph.graph_from_place(PLACE, network_type="walk")
    return G


def get_bus_stops():
    bus = ox.features.features_from_place(PLACE, tags={"highway": "bus_stop"})
    return bus


def get_subway_stops():
    subway = ox.features.features_from_place(
        PLACE, tags={"railway": "station", "station": "subway"})
    return subway


def get_tram_stops():
    tram = ox.features.features_from_place(
        PLACE, tags={"railway": "tram_stop"})
    return tram
