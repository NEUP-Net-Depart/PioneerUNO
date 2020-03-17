import asyncio

import websockets

from src.lobby.WebService import websocket_handler

if __name__ == '__main__':
    server = websockets.serve(websocket_handler, "0.0.0.0", 8080)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
