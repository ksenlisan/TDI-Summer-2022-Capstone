from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = b'cjgfkgeer747^^&%*R'

@app.route("/")
def index():
    return render_template("base.html") 

@app.route("/about")
def home():
    return render_template("about.html")


@app.route('/form', methods = ['POST', 'GET'])
def form():
    if request.method == 'GET':
        return render_template("form.html")     
    if request.method == 'POST':
        value1 = request.form['value1']
        value2 = request.form['value2']
        return redirect(url_for("saferoute", a=value1, b=value2))



if __name__ == "__main__":
    app.run()