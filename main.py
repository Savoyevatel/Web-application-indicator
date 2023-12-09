from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO, emit
import random
from string import ascii_uppercase
from parsing_moveset import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "sasdfkafdslkasdh"
socketio = SocketIO(app)

rooms = {}
messages = []
players = {}
##damage = 0
#health = 1000
#damage_d = 0

def generate_code(length,rooms):
    #gen_code = ''
    while length:
        gen_code = "".join(random.choice(ascii_uppercase) for _ in range(length))
        if gen_code not in rooms:
            break
    return gen_code

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name")

        if join is not False and not code:
            return render_template("home.html", error="Please enter a room code")
        
        room = code
        if create is not False:
            room = generate_code(5,rooms)
            rooms[room] = {"members": 0, "messages": messages}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist")
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    
    if "health" not in rooms[room]:
        rooms[room]["health"] = {session["name"]: 1000}
    

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@app.route('/index')
def index():
    return render_template('index.html')

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")
    print(rooms)


@app.route('/fighting', methods=['POST'])
def fighting():
    name = request.form.get('name')
    return redirect(url_for('fight', name=name))

@app.route('/fight/<name>')
def fight(name):
    moves, img, user = parsing(name)
    socketio.emit('image', {'img': img})

    if moves:
        var1 = moves
        var2 = img
        var3 = user
        
        return render_template('fight.html', var1=var1, var2=var2, var3=var3)

    if not moves:
        return render_template('index.html', error="Please enter a valid pokemon name") 

@socketio.on('attack from player 1')
def handle_attack(data):
    #global players
    #global health
    player_id = session.get("name")
    room = session.get("room")
    #move_name = data['move_name']
    damage = data['damage']
    health = rooms[room]["health"].get(player_id, 1000)  # Assuming initial health is 1000
    health -= damage
    health = max(0, health)  # Ensure health doesn't go below 0
    rooms[room]["health"][player_id] = health

    # Emit health update to all players in the room
    socketio.emit('health_update', {'health': health}, room=room, include_self=False)

if __name__ == "__main__":
    socketio.run(app, debug=True)