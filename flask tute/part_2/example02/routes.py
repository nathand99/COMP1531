from flask import Flask
from server import app

@app.route("/")
def index():
    return "<h1> Hello, World </h1>"

#in this file we will store what happens when user types in different links. Right now, there is just an index (home page) and all that happens when you open the main page is that it prints Hello World
