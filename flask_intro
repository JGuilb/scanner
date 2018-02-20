from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def acceuil():
    return render_template('accueil.html')

@app.route('/result', methods= ['POST', 'GET'])
def result():
    if request.method=='POST':
        result = request.form
        return render_template("Bienvenue.html", result = result)

@app.route('/result/validation', methods = ['POST','GET'])
def validate():
    if request.method == 'POST':
        validate = request.form
        return render_template("Validation.html", validate = validate)
                                             
if __name__ == '__main__':
    app.run()

