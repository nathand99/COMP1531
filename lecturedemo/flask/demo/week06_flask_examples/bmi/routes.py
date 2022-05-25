from flask import Flask,render_template,request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def calculate():
    if request.method == 'POST':
       mass = float(request.form["Mass"])
       height = float(request.form["Height"])
       bmi = mass/(height*height)
       return render_template('bmi.html',bmi="{0:.2f}".format(bmi))
    return render_template('bmi.html')


if __name__ == '__main__':
   app.run(debug=True)
