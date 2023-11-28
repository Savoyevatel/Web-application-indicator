from flask import Flask, render_template, request, redirect, url_for
from parsing_moveset import *
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

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
   
@socketio.on('attack')
def handle_attack(data):
    move_name = data['move_name']
    damage = data['damage']
    player_id = request.sid
    print(f"Player {player_id} used attack: {move_name} with {damage} damage")
    #print(f"Used attack: {move_name} with {damage} damage")
    socketio.emit('update_player_info', {'player_id': player_id, 'health': 50}) 

if __name__ == '__main__':
    app.run(debug=True)
