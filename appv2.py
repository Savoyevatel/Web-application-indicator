from flask import Flask, render_template, request, redirect, url_for
from parsing_moveset import *
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Dictionary to store player data
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

@socketio.on('connect')
def handle_connect():
    player_id = request.sid
    players[player_id] = {'damage_d': 0}
    print(f"Player {player_id} connected")

@socketio.on('disconnect')
def handle_disconnect():
    player_id = request.sid
    del players[player_id]
    print(f"Player {player_id} disconnected")

@socketio.on('attack')
def handle_attack(data):
    player_id = request.sid
    move_name = data['move_name']
    damage = data['damage']

    print(f"Player {player_id} used attack: {move_name} with {damage} damage")

    damage_d = players[player_id]['damage_d']
    damage_d += damage
    players[player_id]['damage_d'] = damage_d
    
    print(players)

    # Emit an event to update other clients with the damage_d value
    emit('update_damage', {'player_id': player_id, 'damage_d': damage_d}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)