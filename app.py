from flask import Flask, render_template, request, redirect, url_for
from parsing_moveset import *
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

#list of players
players = {}
damage = 0

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
    global damage
    move_name = data['move_name']
    curr_damage = data['damage']
    player_id = request.sid
    players[str(player_id)] = damage
    damage += data['damage']
    print(f"Player {player_id} used attack: {move_name} with {curr_damage} damage")
    players[str(player_id)] = damage
    print(players)

if __name__ == '__main__':
    socketio.run(app, debug=True)
