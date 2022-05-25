from flask import Flask

#create an application instance
app = Flask(__name__)


@app.route("/")
def index():
    return " <h1> Hello World! </h1> "

@app.route("/<name>")
def user(name):
    return "<h1> Hello there {0} </h1>".format(name)

if __name__=='__main__':
   app.run()
