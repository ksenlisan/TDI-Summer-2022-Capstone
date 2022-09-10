from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
import folium

app = Flask(__name__)
app.secret_key = b'cjgfkgeer747^^&%*R'

@app.route("/")
def index():
    return render_template("base.html") 

@app.route("/about")
def home():
    return render_template("about.html")

@app.route("/show_map")
def show_map():
    map = folium.Map(location=[34.09,-118.36], zoom_start=14, width=750, height=500)
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
        return 'Please enter valid address'
    new_line = '\n'
    map = folium.Map(location=[34.09,-118.36], zoom_start=14, width=750, height=500)


    return f'Starting coordinates: {from_location} long/lat: {from_location.longitude}, {from_location.latitude} {new_line} Destination coordinates: {to_location} long/lat {to_location.longitude}, {to_location.latitude}'





if __name__ == "__main__":
    app.run()