from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"

#You have now initialised your application. From now on, to interact with the application, you will use
#the app object. In the next line, you will also notice that we have configured the flask application
#instance with a secret key. 
