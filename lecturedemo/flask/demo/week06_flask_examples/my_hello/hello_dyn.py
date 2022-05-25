from flask import Flask, request, redirect,render_template,url_for

#create an application instance
app = Flask(__name__)

#register a function index() as the handler for the application's root URL
#functions like index are called as the view function
#application needs to know what code to run for each URL requested
#so it keeps a mapping of the URL to a function
#the association between a URL and a function is called a route

@app.route('/', methods=["GET","POST"])
def index():
	if request.method == 'POST':
		name = request.form["name"]
		zID = int(request.form["zID"])
		desc = request.form["desc"]
		return render_template('hello.html',name=name,zID=zID,desc=desc)
	return	render_template('input.html')

@app.route('/<name>')
def user(name):
	return '<h1>Hello {0} </h1>'.format(name)

if __name__=='__main__':
	app.run(debug=True)
