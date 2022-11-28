from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
import folium
from folium import plugins
import pickle
import osmnx as ox
import networkx as nx


app = Flask(__name__)
app.secret_key = b'cjgfkgeer747^^&%*R'

# load base html template
# other html templates are an extension of this one
@app.route("/")
def index():
    return render_template("base.html") 

# load introduction page
@app.route("/introduction")
def introduction():
    return render_template("introduction.html") 

# load about page
@app.route("/about")
def home():
    return render_template("about.html")

# display saved crime points from file to an html map
@app.route("/show_map")
def show_map():
    with open ('crimes_data', 'rb') as fp:
        crimes = pickle.load(fp)
    locations = [x[::-1] for x in crimes]
    map = folium.Map(location=[34.09,-118.36], zoom_start=14, width=750, height=500)
    cluster = plugins.MarkerCluster(locations=locations)  
    map.add_child(cluster)
    return map._repr_html_()

#get user input for points of origin and destination
@app.route('/form', methods = ['POST', 'GET'])
def form():
    if request.method == 'GET':
        return render_template("form.html")     
    if request.method == 'POST':
        value1 = request.form['value1']
        value2 = request.form['value2']
        return redirect(url_for("saferoute", a=value1, b=value2))
     
# functional part of the app
# Returns crime-weighted route plotted on a map
@app.route('/saferoute?<a>&<b>')
def saferoute(a, b):
    # User imput check
    # use a nominatim service to match input with a valid address/location
    geolocator = Nominatim(user_agent="decomposition.of.life@gmail.com")
    from_location = geolocator.geocode(a)
    to_location = geolocator.geocode(b)

    # if entered text cannot be interpreted as a valid location the error message will appear
    if from_location == None or to_location == None:
        return 'The address you entered is not valid.' 

    # Load WeHo graph
    G_walk = ox.graph_from_place('West Hollywood, Los Angeles County, California, United States',
                             network_type='walk')
                             
    #find nearest node for target addresses and distance between entered point and node
    orig_node, orig_dist = ox.distance.nearest_nodes(G_walk, from_location.longitude, from_location.latitude, return_dist=True)
    dest_node, dest_dist = ox.distance.nearest_nodes(G_walk, to_location.longitude, to_location.latitude, return_dist=True)

    # Checks if user input is within WeHo area, returns error message if not
    if orig_dist > 100 or dest_dist > 100:
        return 'The address you entered is not in West Hollywood.'

    #create map
    map = folium.Map(location=[34.09,-118.36], zoom_start=14, width=750, height=500)
    #load edge weights
    with open('edges_weights_crime', 'rb') as fp:
        edges_weights_crime = pickle.load(fp)
    # add edge weights to graph
    G_walk.add_weighted_edges_from(edges_weights_crime, 'weight')
    orig_node = ox.distance.nearest_nodes(G_walk, from_location.longitude, from_location.latitude)
    dest_node = ox.distance.nearest_nodes(G_walk, to_location.longitude, to_location.latitude)

    # generate route between 2 points
    route2 = nx.shortest_path(G_walk, #returns a sequence of nodes
                            orig_node,
                            dest_node,
                            weight='weight')

    # Compute route length
    # for some reason G_walk needs to be created again otherwise KeyError 'length'                        
    G_walk = ox.graph_from_place('West Hollywood, Los Angeles County, California, United States',
                             network_type='walk')
    total_length = f'Total length of this route: {int(sum(ox.utils_graph.get_route_edge_attributes(G_walk, route2, attribute="length")))} meters'
    
    #add route to map
    ox.plot_route_folium(G_walk, route2, map)

    # include route length in the title
    title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(total_length)   
    map.get_root().html.add_child(folium.Element(title_html))     

    # add markers for origin and destination on map
    folium.Marker(location=[from_location.latitude, from_location.longitude],popup = from_location,
                icon= folium.Icon(color='green')).add_to(map)
    folium.Marker(location=[to_location.latitude, to_location.longitude],popup = to_location,
                icon= folium.Icon(color='blue')).add_to(map)

    # return map to be displayed on the web page
    return render_template('result.html', map=map._repr_html_())

# run app
if __name__ == "__main__":
    app.run(debug=True)