import folium
from folium import plugins
import osmnx as ox
import networkx as nx
import shapely
import geopandas as gpd
from shapely.geometry import CAP_STYLE, JOIN_STYLE, LineString
import numpy as np
from geopy.geocoders import Nominatim
import pickle


#load crimes
with open ('crimes_data', 'rb') as fp:
    crimes = pickle.load(fp)
#load edges weights
with open ('edges_weights_crime', 'rb') as fp:
    edges_weights_crime = pickle.load(fp)


user_origin = "692 N Robertson Blvd, West Hollywood, CA 90069"
user_destination = "7871 Santa Monica Blvd, West Hollywood, CA 90046"


#get address coordinates
def address_to_longlat(address):     
    geolocator = Nominatim(user_agent="decomposition.of.life@gmail.com")
    location = geolocator.geocode(address)
    return location.longitude, location.latitude

orig_long, orig_lat = address_to_longlat(user_origin)
dest_long, dest_lat = address_to_longlat(user_destination)

#create route
ox.config.log_console=True
ox.config.use_cache=True
G_walk = ox.graph_from_place('West Hollywood, Los Angeles County, California, United States',
                             network_type='walk')

G_walk.add_weighted_edges_from(edges_weights_crime, 'weight')

#create graph with weighted edges
orig_node = ox.distance.nearest_nodes(G_walk,orig_long, orig_lat)
dest_node = ox.distance.nearest_nodes(G_walk, dest_long, dest_lat)


route2 = nx.shortest_path(G_walk, #returns a sequence of nodes
                         orig_node,
                         dest_node,
                         weight='weight')
#create a map
m_dt = folium.Map(location=[34.09,-118.36], zoom_start=14)

#add route to map
route_map = ox.plot_route_folium(G_walk, route2, m_dt)
