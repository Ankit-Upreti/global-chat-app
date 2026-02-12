import asyncio
import websockets
import os
import json
import hashlib

USERS_FILE = "users.json"

connected_clients = {}
users_db = {}


def load_users():
    global users_db
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users_db = json.load(f)


def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


async def handler(websocket):
    login_data = json.loads(await websocket.recv())
    username = login_data["username"]
    password = hash_password(login_data["password"])

    # Register or authenticate
    if username not in users_db:
        users_db[username] = password
        save_users()
        await websocket.send(json.dumps({"status": "registered"}))
    else:
        if users_db[username] != password:
            await websocket.send(json.dumps({"status": "denied"}))
            return
        await websocket.send(json.dumps({"status": "authenticated"}))

    connected_clients[websocket] = username
    print(f"{username} connected")

    try:
        async for message in websocket:
            data = {
                "user": username,
                "message": message
            }

            for client in connected_clients:
                if client != websocket:
                    await client.send(json.dumps(data))

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        print(f"{username} disconnected")
        del connected_clients[websocket]


async def main():
    load_users()
    port = int(os.environ.get("PORT", 10000))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Server running on port {port}")
        await asyncio.Future()


asyncio.run(main())

