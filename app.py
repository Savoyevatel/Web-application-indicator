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

    else:
        return redirect(url_for('index')) 

@socketio.on('attack')
def handle_attack_P(data):
    player_id = request.sid
    player_health = 1000
    move_name = data['move_name']
    damage = data['damage']
    print(f"Received from Player {player_id}: {damage}")
    print(f"Player {player_id} used attack: {move_name} with {damage} damage")
    player2_health -= damage
    print(f"Player 2 current health after {move_name} is {player2_health}")
    #health = players.get(player_id, {'health': 100})['health']
    #health -= damage
    #health = max(0, health)
    #players[player_id] = {'health': health}

    #socketio.emit('update_player_2', {'player_id': player_id, 'health': health})
    #socketio.emit('message_to_player2', damage, broadcast=True)
    socketio.emit('message_to_player2', damage)
    socketio.emit('update_health', player2_health)

if __name__ == '__main__':
    app.run(debug=True)
