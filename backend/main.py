from fastapi import Depends, FastAPI , HTTPException ,Response, Cookie ,WebSocket, WebSocketDisconnect
from Send_mail.send_mail import get_friends, send_email

from models.user import create_tables
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from pydantic import BaseModel
from db.db import get_db
from auth import auth
from Send_Live_Location.live_laction import add_websocket
create_tables()
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://crispy-space-acorn-jj59jvrp5wxqhp69r-5173.app.github.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class LocationRequest(BaseModel):
    lat: float
    lng: float



@app.get("/")
def main():
    return {
        "message": "Welcome to Aegis SOS Alert System"
    }


@app.post("/send_mail")
async def send_mail(data: LocationRequest,user:dict=Depends(auth.get_current_user)):
    mail_list=get_friends(user['id'])
    location = f"https://maps.google.com/?q={data.lat},{data.lng}"
    output=  send_email(mail_list, "SOS Alert", "keshav", location)
    return {
        "message": "Mails sent successfully",
        "output": output
    }

@app.post("/signup")
def signup(data:dict):
    data["password"]=auth.get_password_hash(data['password'])
    conn = get_db()
    try:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, email, community_saver, password) VALUES (?, ?, ?, ?)", (data['username'], data['email'], data['community_saver'], data['password']))
        conn.commit()
         
        return {"message": "User created successfully"}
    except Exception as e:
         
        raise HTTPException(status_code=400, detail= {"message": "User creation failed", "error": str(e)})
    finally:
        conn.close()   

@app.post("/login")
def login(data:dict):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE  username= ? ",  (data['username'],))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=400, detail= {"message": "Invalid username or password"})
    
    user=auth.authenticate_user(data['username'], data['password'])
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token_expire = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    token=auth.create_access_token(data={"sub": user['username']}, expires_delta=access_token_expire)
    response = Response(content="Login successful")
    print("Generated token for user:", user['username'], "Token:", token)
    response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,
    samesite="none",
    max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
)

    return response


@app.websocket("/ws/location")
async def location_socket(websocket: WebSocket,user:dict=Depends(auth.get_current_user)):
    await add_websocket(websocket,user['id'])


    
@app.post("/add_friend")
def add_friend(data:dict):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (data['username'],))
    user_id = cursor.fetchone()
    cursor.execute("SELECT id FROM users WHERE username = ?", (data['friend_username'],))
    friend_id = cursor.fetchone()
    if not user_id or not friend_id:
        raise HTTPException(status_code=400, detail="User not found")
    
    try:
        cursor.execute("INSERT INTO friends (user_id, friend_id) VALUES (?, ?)", (user_id[0], friend_id[0]))
        conn.commit()
        return {"message": "Friend added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": "Failed to add friend", "error": str(e)})
    finally:
        conn.close()
     