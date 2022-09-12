from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
import folium
from folium import plugins
import pickle
import osmnx as ox
import networkx as nx

app = Flask(__name__)
app.secret_key = b'cjgfkgeer747^^&%*R'

@app.route("/")
def index():
    return render_template("base.html") 

@app.route("/introduction")
def introduction():
    return render_template("introduction.html") 

@app.route("/about")
def home():
    return render_template("about.html")

@app.route("/show_map")
def show_map():
    with open ('crimes_data', 'rb') as fp:
        crimes = pickle.load(fp)
    locations = [x[::-1] for x in crimes]
    map = folium.Map(location=[34.09,-118.36], zoom_start=14, width=750, height=500)
    cluster = plugins.MarkerCluster(locations=locations)  
    map.add_child(cluster)
    return map._repr_html_()

@app.route('/form', methods = ['POST', 'GET'])
def form():
    if request.method == 'GET':
        return render_template("form.html")     
    if request.method == 'POST':
        value1 = request.form['value1']
        value2 = request.form['value2']
        return redirect(url_for("saferoute", a=value1, b=value2))
     

@app.route('/saferoute?<a>&<b>')
def saferoute(a, b):
    geolocator = Nominatim(user_agent="decomposition.of.life@gmail.com")
    from_location = geolocator.geocode(a)
    to_location = geolocator.geocode(b)
    if from_location == None or to_location == None:
        return 'Please enter valid address' #will need to add html form with error mssg

    map = folium.Map(location=[34.09,-118.36], zoom_start=14, width=750, height=500)

    #load edge weights
    with open('edges_weights_crime', 'rb') as fp:
        edges_weights_crime = pickle.load(fp)

    G_walk = ox.graph_from_place('West Hollywood, Los Angeles County, California, United States',
                             network_type='walk')

    G_walk.add_weighted_edges_from(edges_weights_crime, 'weight')
    #maybe save G-walk as file?

    #create graph with weighted edges
    orig_node = ox.distance.nearest_nodes(G_walk, from_location.longitude, from_location.latitude)
    dest_node = ox.distance.nearest_nodes(G_walk, to_location.longitude, to_location.latitude)


    route2 = nx.shortest_path(G_walk, #returns a sequence of nodes
                            orig_node,
                            dest_node,
                            weight='weight')
    #for some reason G_walk needs to be created again otherwise KeyError 'length'                        
    G_walk = ox.graph_from_place('West Hollywood, Los Angeles County, California, United States',
                             network_type='walk')
    #add route to map
    ox.plot_route_folium(G_walk, route2, map)
    

    return (map._repr_html_())
#    return f'Starting coordinates: {from_location} long/lat: {from_location.longitude}, {from_location.latitude} {new_line} Destination coordinates: {to_location} long/lat {to_location.longitude}, {to_location.latitude}'





if __name__ == "__main__":
    app.run(debug=True)