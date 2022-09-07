from flask import Flask, render_template, request, flash
import folium

app = Flask(__name__)
app.secret_key = b'cjgfkgeer747^^&%*R'

@app.route("/")
def home():
    map = folium.Map(location=[34.09,-118.36], zoom_start=14)
    return map._repr_html_()

@app.route("/main")
def index():
    flash("Say something")
    return render_template("html_template.html") 

if __name__ == "__main__":
    app.run()