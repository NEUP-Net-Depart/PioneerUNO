import json

import aiohttp
from aiohttp import web

from src.PioneerUno.Player import Player
from src.PioneerUno.Response import respond_success, unknown_command, missing_parameters_error
from src.PioneerUno.Room import get_all_room, add_room

app = web.Application()
routes = web.RouteTableDef()


@routes.get("/api/ping")
async def pong(request):
    return web.Response(text="pong")


@routes.get("/api/rooms")
async def get_rooms(request):
    return web.json_response(respond_success(get_all_room()))


def handle_create_room(player):
    new_room = add_room()
    new_room.add_player(player)
    return respond_success(new_room.id)


def handle_ping(player):
    return respond_success('pong')


command_handler = {
    "create_room": handle_create_room,
    "ping": handle_ping,
}


@routes.get("/api/ws")
async def websocket_handler(request):
    try:
        nickname = request.query['nickname']
    except KeyError:
        return web.json_response(missing_parameters_error)

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    player = Player(nickname, ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            msg_json = json.loads(msg.data)
            try:
                await ws.send_json(command_handler[msg_json['command']](player))
            except:
                await ws.send_json(unknown_command)
                raise
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(ws.exception())
            break

    player.leave_room()
    print("disconnected")


app.add_routes(routes)
