import asyncio
import websockets
import json
import sys
import getpass

uri = "wss://chaton-4i6d.onrender.com"




async def send_message(websocket):
    loop = asyncio.get_event_loop()
    while True:
        message = await loop.run_in_executor(None, input, "")
        await websocket.send(message)


async def receive_message(websocket):
    async for message in websocket:
        data = json.loads(message)
        sys.stdout.write(f"\r{data['user']}: {data['message']}\n")
        sys.stdout.flush()


async def main():
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    async with websockets.connect(uri) as websocket:

        login_payload = {
            "username": username,
            "password": password
        }

        await websocket.send(json.dumps(login_payload))

        response = json.loads(await websocket.recv())

        if response["status"] == "denied":
            print("Authentication failed.")
            return

        if response["status"] == "already_logged_in":
            print("User already logged in elsewhere.")
            return


        print("Login successful.")

        await asyncio.gather(
            send_message(websocket),
            receive_message(websocket)
        )


asyncio.run(main())

