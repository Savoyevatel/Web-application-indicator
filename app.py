from flask import Flask, render_template, request, redirect, url_for
from parsing_moveset import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form.get('name')
    return redirect(url_for('greeting', name=name))

@app.route('/greeting/<name>')
def greeting(name):
    moves, img, user = parsing(name)

    if moves:
        var1 = moves
        var2 = img
        var3 = user
        return render_template('greeting.html', var1=var1, var2=var2, var3=var3)

    else:
        return redirect(url_for('index'))    
   
if __name__ == '__main__':
    app.run(debug=True)
