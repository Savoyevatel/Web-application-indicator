from flask import Flask, render_template, request, redirect, url_for
from parsing_moveset import *
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

#list of players
players = {}

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

    if not moves:
        return render_template('index.html', error="Please enter a valid pokemon name") 
        #return redirect(url_for('index')) 

@socketio.on('attack from player 1')
def handle_attack(data):
    global players
    move_name = data['move_name']
    damage = data['damage']
    player_id = request.sid

    print(f"Player {player_id} used attack: {move_name} with {damage} damage")

    damage_d = players.get(player_id, {'damage_d': 0})['damage_d']
    damage_d += damage
    players[player_id] = {'damage_d': damage_d}
 
    #socketio.emit('update_player_info', {'player_id': player_id, 'health': health})
    #socketio.emit(health, to=greeting)
    print(players)
    players = {key: {'damage_d': value['damage_d']} for key, value in players.items()}
    print(players)
if __name__ == '__main__':
    socketio.run(app, debug=True)
