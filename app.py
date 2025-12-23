from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
import time, uuid, random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'high-five-vibe-ultra-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage (Restarting server clears this)
users = {} 
waiting_queue = []
active_rooms = {}
stats = {"total_high_fives": 0, "online": 0}

@app.route('/')
def index():
    if 'username' not in session: return redirect(url_for('login_page'))
    return render_template('index.html', username=session['username'], social=session['social'])

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['social'] = request.form.get('social')
        session['platform'] = request.form.get('platform')
        session['vibe'] = request.form.get('vibe')
        session['streak'] = 0
        return redirect(url_for('index'))
    return render_template('login.html')

@socketio.on('connect')
def handle_connect():
    stats["online"] += 1
    if 'username' in session:
        users[request.sid] = {
            'username': session['username'],
            'social': session['social'],
            'platform': session['platform'],
            'vibe': session['vibe'],
            'streak': session.get('streak', 0)
        }
    emit('update_stats', stats, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    stats["online"] = max(0, stats["online"] - 1)
    if request.sid in waiting_queue: waiting_queue.remove(request.sid)
    emit('update_stats', stats, broadcast=True)

@socketio.on('find_match')
def handle_find_match():
    user_id = request.sid
    if user_id in waiting_queue: return
    
    if len(waiting_queue) > 0:
        partner_id = waiting_queue.pop(0)
        room_id = str(uuid.uuid4())
        join_room(room_id, sid=user_id); join_room(room_id, sid=partner_id)
        
        end_time = time.time() + 300
        active_rooms[room_id] = {
            'users': {user_id: False, partner_id: False},
            'data': {user_id: users[user_id], partner_id: users[partner_id]}
        }
        
        emit('match_success', {'room_id': room_id, 'initiator': True, 'end_time': end_time, 'partner': users[partner_id]}, room=user_id)
        emit('match_success', {'room_id': room_id, 'initiator': False, 'end_time': end_time, 'partner': users[user_id]}, room=partner_id)
    else:
        waiting_queue.append(user_id)

@socketio.on('give_high_five')
def handle_high_five(data):
    room_id = data['room_id']
    if room_id in active_rooms:
        active_rooms[room_id]['users'][request.sid] = True
        if all(active_rooms[room_id]['users'].values()):
            stats["total_high_fives"] += 1
            emit('mutual_match', {'handles': active_rooms[room_id]['data']}, room=room_id)
            emit('update_stats', stats, broadcast=True)

@socketio.on('nuke_triggered')
def handle_nuke(data):
    games = [
        "MINI-GAME: Truth or Dare! Initiator goes first.",
        "MINI-GAME: Would you rather? (Pizza for life vs Tacos for life)",
        "ICEBREAKER: What is the weirdest dream you ever had?",
        "GAME: Roleplay! You are both astronauts stuck on Mars."
    ]
    emit('topic_nuke', {'topic': random.choice(games)}, room=data['room_id'])

@socketio.on('signal')
def handle_signal(data):
    emit('signal', data, room=data['room_id'], include_self=False)

@socketio.on('report_user')
def handle_report(data):
    # Immediate Nuke: Terminate for both
    emit('security_terminate', {'msg': 'Connection closed for safety.'}, room=data['room_id'])

if __name__ == '__main__':
    socketio.run(app, debug=True)