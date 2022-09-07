from flask import Flask
import folium

app = Flask(__name__)

@app.route("/")
def home():
    map = folium.Map(location=[34.09,-118.36], zoom_start=14)
    return map._repr_html_()

@app.route("/<name>")
def user(name):
    return f"Hello {name}"

if __name__ == "__main__":
    app.run()