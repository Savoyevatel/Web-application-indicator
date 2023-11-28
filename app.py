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
   
@socketio.on('attack from player 1')
def handle_attack_P1(data):
    move_name = data['move_name']
    damage = data['damage']
    player_id = request.sid
    print(f"Player {player_id} used attack: {move_name} with {damage} damage")
    #health = players.get(player_id, {'health': 100})['health']
    #health -= damage
    #health = max(0, health)
    #players[player_id] = {'health': health}

    #socketio.emit('update_player_2', {'player_id': player_id, 'health': health})
    #socketio.emit('message_to_player2', damage, broadcast=True)
    socketio.emit('message_to_player2', damage)

@socketio.on('attack from player 2')
def handle_attack_P2(data):
    damage = data['damage']
    socketio.emit('message_to_player1', damage)

if __name__ == '__main__':
    app.run(debug=True)