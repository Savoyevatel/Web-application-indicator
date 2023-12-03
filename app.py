from flask import Flask, render_template, request, redirect, url_for
from parsing_moveset import *
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

players = {}
damage = 0
health = 1000
damage_d = 0

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

@socketio.on('attack from player 1')
def handle_attack(data):
    global players
    global health
    player_id = request.sid
    print(player_id)
    move_name = data['move_name']
    damage = data['damage']

    print(f"Player {player_id} used attack: {move_name} with {damage} damage")

    damage_d = players.get(player_id, {'damage_d': 1000})['damage_d']
    damage_d -= damage
    players[player_id] = {'damage_d': damage_d}
    health -= damage_d
    health = max(0,health)
    emit('update_health', {'damage_d': damage_d}, room=player_id)



if __name__ == '__main__':
    socketio.run(app, debug=True)
