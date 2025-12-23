from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import time
import uuid

app = Flask(__name__)
# standard configuration for local development
app.config['SECRET_KEY'] = 'high-five-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# --- GAME STATE ---
# In a real production app, use Redis. For MVP, memory is fine.
waiting_queue = [] 
active_rooms = {} 

@socketio.on('connect')
def handle_connect():
    print(f"User connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"User disconnected: {request.sid}")
    
    # 1. Remove from waiting queue if they are there
    if request.sid in waiting_queue:
        waiting_queue.remove(request.sid)
    
    # 2. Notify their partner if they were in an active call
    # (Logic to find room and notify partner goes here)

@socketio.on('find_match')
def find_match():
    """
    The core logic: If someone is waiting, match them.
    If no one is waiting, put this user in the queue.
    """
    user_id = request.sid
    
    if len(waiting_queue) > 0:
        # --- MATCH FOUND! ---
        partner_id = waiting_queue.pop(0)
        
        # Create a unique room for these two
        room_id = str(uuid.uuid4())
        
        # Group them together using SocketIO 'rooms'
        join_room(room_id, sid=user_id)
        join_room(room_id, sid=partner_id)
        
        # Calculate hard stop time (5 minutes from now)
        start_time = time.time()
        end_time = start_time + 300  # 300 seconds = 5 mins
        
        # Store room data
        active_rooms[room_id] = {
            'users': [user_id, partner_id],
            'end_time': end_time
        }
        
        # Tell both users: "GO!"
        # We send 'initiator: true' to one so they know to start the WebRTC offer
        socketio.emit('match_success', {
            'room_id': room_id,
            'partner_id': partner_id,
            'end_time': end_time,
            'initiator': False
        }, room=partner_id)
        
        socketio.emit('match_success', {
            'room_id': room_id,
            'partner_id': user_id,
            'end_time': end_time,
            'initiator': True
        }, room=user_id)
        
        print(f"Matched {user_id} with {partner_id} in room {room_id}")
        
    else:
        # --- NO MATCH YET, PLEASE WAIT ---
        waiting_queue.append(user_id)
        emit('waiting_for_match', {'message': 'Looking for a High Five...'})
        print(f"User {user_id} added to queue.")

@socketio.on('nuke_triggered')
def handle_nuke(data):
    """
    When one client detects silence, they tell the server.
    The server tells EVERYONE in that room to display the topic.
    """
    room_id = data['room_id']
    import random
    topics = [
        "Conspiracy: Why do pigeons bob their heads?",
        "Roleplay: You are both distinct flavors of soup.",
        "Debate: Is a hotdog a sandwich? Go!"
    ]
    chosen_topic = random.choice(topics)
    
    # Broadcast to the specific room only
    emit('topic_nuke_display', {'topic': chosen_topic}, room=room_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)