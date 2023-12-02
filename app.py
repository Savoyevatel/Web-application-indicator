from flask import Flask, render_template, request, redirect, url_for
from parsing_moveset import *
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

#list of players
players = {}
ini_damage = 0
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
    move_name = data['move_name']
    damage = data['damage']
    player_id = request.sid
    players[str(player_id)] = damage
    print(players)

    print(f"Player {player_id} used attack: {move_name} with {damage} damage")
    players[player_id] += damage
    damage = data['damage']
    print(players)
    '''
    health = players.get(player_id, {'health': 1000})['health']

    damage_d = players.get(player_id, {'damage_d': 0})['damage_d']
    damage_d += damage
    health -= damage

    health = max(0, health)

    players[player_id] = {'health': health}
    players[player_id]['damage_d'] = damage_d
    print(players)
    print(health)
    socketio.emit('update_player_info', health)
    #socketio.emit(health, to=greeting)
    #socketio.emit(health, {'health': health}, namespace='/greeting')
    '''
    
if __name__ == '__main__':
    socketio.run(app, debug=True)
