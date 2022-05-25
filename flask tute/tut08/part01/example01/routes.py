from flask import Flask, redirect, render_template, request, url_for
from server import app, user_input

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        zID = int(request.form["zID"])
        desc = request.form["desc"]
        user_input.append([name, zID, desc])
        return redirect(url_for('hello'))
    return render_template("index.html")

@app.route("/Hello")
def hello():
    name = user_input[0][0]
    id=user_input[0][1]
    desc=user_input[0][2]
    return render_template("hello.html", name=name, id=id, desc=desc)
