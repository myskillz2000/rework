from flask import Flask, render_template
from graphviz import render
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("base.html")

@app.route("/home")
def hello_world():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)