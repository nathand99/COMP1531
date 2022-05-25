from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def calculate():
    if request.method == 'POST':
       mass = float(request.form["Mass"])
       height = float(request.form["Height"])
       name = request.form["Name"]
       bmi = mass/(height*height)
       return redirect(url_for("display", name=name, bmi="{0:.2f}".format(bmi))) 
    return render_template('bmi.html')
    
@app.route("/result/<name>/<bmi>")
def display(name, bmi):
    return render_template("result.html", name=name, bmi=float(bmi))

if __name__ == '__main__':
   app.run(debug=True, port="1333")
