import json

import aiohttp
from aiohttp import web

from src.lobby.Adaptor import deserialize_card
from src.lobby.Message import *
from src.lobby.Player import Player
from src.lobby.Room import get_all_room, add_room, rooms

app = web.Application()
routes = web.RouteTableDef()


@routes.get("/api/ping")
async def pong(request):
    return web.Response(text="pong")


@routes.get("/api/rooms")
async def get_rooms(request):
    return web.json_response(respond_success(get_all_room()))


async def handle_create_room(player, data):
    new_room = add_room(data.get('max_player', 2))
    await new_room.add_player(player)
    return respond_success(new_room.id)


async def handle_ping(player, data):
    return respond_success('pong')


async def handle_join_room(player, data):
    if player.room is not None:
        return already_in_room

    try:
        room = rooms[data['id']]
    except KeyError:
        return unknown_room_id

    try:
        await room.add_player(player)
    except:
        return room_is_full
    return respond_success([
        player.get_name()
        for player in room.players.values()
    ])


async def handle_leave_room(player, data):
    await player.leave_room()
    return respond_success()


async def handle_toggle_prepare_state(player, data):
    await player.toggle_preparing_state(data.get('state', False))
    return respond_success()


async def handle_put_card(player, data):
    await player.put_card(deserialize_card(data))
    return respond_success()


async def handle_skip_turn(player, data):
    await player.skip_turn()
    return respond_success()


async def handle_cut_card(player, data):
    await player.cut_card(deserialize_card(data))
    return respond_success()


command_handler = {
    "create_room": handle_create_room,
    "join_room": handle_join_room,
    "leave_room": handle_leave_room,
    "toggle_prepare_state": handle_toggle_prepare_state,
    "ping": handle_ping,
    "put_card": handle_put_card,
    "skip_turn": handle_skip_turn,
    "cut_card": handle_cut_card
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
            data = msg_json.get('data', None)
            try:
                result = await command_handler[msg_json['command']](player, data)
                await ws.send_json(result)
            except:
                await ws.send_json(unknown_command)
                raise
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(ws.exception())
            break

    await player.leave_room()
    print("disconnected")


app.add_routes(routes)
