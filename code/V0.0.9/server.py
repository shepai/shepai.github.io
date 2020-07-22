from AI import CB
import sys
import asyncio
import websockets
import threading

async def Reply(websocket, path):
    cleverBot=CB(sys.path[0].replace("\\","/")+"/testCB/")
    try:
        print("User Connected", websocket)
        async for message in websocket:
            m=cleverBot.chat(message)
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
            print("User disconnected", websocket)
            cleverBot=None

print("SHEP SERVER AI")
print("V 0.0.9")
print("*************************")
asyncio.get_event_loop().run_until_complete(
websockets.serve(Reply, port=50101)) #listen for clients
asyncio.get_event_loop().run_forever()
