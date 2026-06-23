from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from math import radians, sin, cos, sqrt, atan2
from db.db import get_db
import json

active_connections = {}
location_store = {}

def find_user_id_from_username(username):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def  get_friends(user_id):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT friend_id FROM friends WHERE user_id = ?", (user_id,))
    friends = [row[0] for row in cursor.fetchall()]
    conn.close()
    return friends

def distance_km(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (sin(dlat/2)**2 +
         cos(radians(lat1)) *
         cos(radians(lat2)) *
         sin(dlon/2)**2)

    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


def nearby_friends(user_id1, long, lat):
    frnds=[]
    for user_id, location in location_store.items():
        if user_id != user_id1:
            if distance_km(lat, long, location["lat"], location["lng"]) <= 1:
                frnds.append(user_id)
    return frnds

async def add_websocket(websocket: WebSocket, user_id: int):
    token = websocket.query_params.get("token")
    
    user_id = user_id if user_id is not None else find_user_id_from_username(token)
    print("Received token:", token, "Mapped user_id:", user_id)

    if not user_id:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    active_connections[user_id] = websocket

    print(f"User {user_id} connected")

    try:
        while True:

            message = await websocket.receive_text()
            data = json.loads(message)

            message_type = data.get("type")

            # User stopped sharing
            if message_type == "stop_sharing":
                print(f"User {user_id} stopped sharing")
                break
            
            
            # Location update
            if message_type == "location":
                location_payload = {
                    "type": "location_update",
                    "user_id": user_id,
                    "lat": data["lat"],
                    "lng": data["lng"],
                }
                print(f"User {user_id} sent location update")
                
                location_store[user_id] = location_payload
                

            elif message_type == "sos_alert" or message_type == "sos_update":
                 
                
                location_payload = {
                    "type": "sos_update" if message_type == "sos_update" else "sos_alert",
                    "user_id": user_id,
                    "lat": data["lat"],
                    "lng": data["lng"],
                }
                location_store[user_id] = {
                    "lat": data["lat"],
                    "lng": data["lng"]
                }

                friends = nearby_friends(user_id, data["lng"], data["lat"])
                print("location_store =", location_store)
                print("friends =", friends)
                

                for friend_id in friends:
                    print(f"User {user_id} sent an SOS alert/update to friends: {friend_id}")

                    friend_socket = active_connections.get(friend_id)

                    if friend_socket:
                        await friend_socket.send_json(
                            location_payload
                        )

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")

    finally:
        active_connections.pop(user_id, None)


