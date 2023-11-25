from flask import Flask, render_template
from flask_socketio import SocketIO
from parsing_moveset import parsing

app = Flask(__name__)
socketio = SocketIO(app)
moves, img, user = parsing()

@app.route('/')
def index():
    var1 = moves
    var2 = img
    var3 = user
    return render_template('index.html', var1=var1, var2=var2, var3=var3)
#    return render_template('index.html', moves, img)

@socketio.on('attack')
def handle_attack(data):
    move_name = data['move_name']
    damage = data['damage']
    print(f"Received attack: {move_name} with {damage} damage")

if __name__ == '__main__':
    socketio.run(app, debug=True)