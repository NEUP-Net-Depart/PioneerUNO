import asyncio
import json
from time import time

import aiohttp
from aiohttp import web

from src.game.rules.GameError import *
from src.lobby.Adaptor import deserialize_card
from src.lobby.Decoration import catch_put_exceptions
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
    new_room = add_room(data.get('max_player', 2), data.get('initial_card_amount', 10))
    await new_room.add_player(player)
    return respond_success({
        'id': new_room.id
    })


async def handle_ping(player, data):
    player.last_time_active = time()
    return respond_success({
        'data': 'pong'
    })


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
    return respond_success(
        {
            "players": [
                player.get_name()
                for player in room.players.values()
            ]
        }
    )


async def handle_leave_room(player, data):
    await player.leave_room()
    return respond_success()


async def handle_toggle_prepare_state(player, data):
    await player.toggle_preparing_state(data.get('state', False))
    return respond_success()


@catch_put_exceptions
async def handle_put_card(player, data):
    await player.put_card(deserialize_card(data))
    return respond_success()


async def handle_skip_turn(player, data):
    try:
        await player.skip_turn()
    except PlayerPassWithoutAction:
        return

    return respond_success()


@catch_put_exceptions
async def handle_cut_card(player, data):
    try:
        await player.cut_card(deserialize_card(data))
    except PlayerPutBlackCardError:
        return put_black_card
    except PlayerCutCardsNotEqualToCurrentError:
        return cut_card_not_equal

    return respond_success()


async def handle_uno(player, data):
    await player.uno


async def handle_get_rooms(*args, **kwargs):
    return respond_success(
        {
            'rooms': get_all_room()
        })


async def handle_chat(player, data):
    message = data.get("message", "")
    await player.chat(message)
    return respond_success()


async def monitor_connection(player):
    while True:
        if time() - player.last_time_active >= 10:
            break
        await asyncio.sleep(10)
    print("time out")


async def receive_message(player):
    while True:
        msg = await player.conn.receive()
        if msg.type == aiohttp.WSMsgType.TEXT:
            msg_json = json.loads(msg.data)
            data = msg_json.get('data', None)
            try:
                result = await command_handler[msg_json['command']](player, data)
                result['requestId'] = msg_json.get('requestId', None)
                await player.conn.send_json(result)
            except Exception as e:
                print(e)
                await player.conn.send_json(unknown_command)

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(player.conn.exception())
            break


command_handler = {
    "create_room": handle_create_room,
    "join_room": handle_join_room,
    "leave_room": handle_leave_room,
    "toggle_preparation_state": handle_toggle_prepare_state,
    "ping": handle_ping,
    "put_card": handle_put_card,
    "skip_turn": handle_skip_turn,
    "cut_card": handle_cut_card,
    "uno": handle_uno,
    "rooms": handle_get_rooms,
    "char": handle_chat,
}


@routes.get("/api/ws")
async def websocket_handler(request):
    try:
        nickname = request.query['nickname']
    except KeyError:
        return web.json_response(missing_parameters_error)

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("get connection" + nickname)
    player = Player(nickname, ws)

    monitor = asyncio.create_task(monitor_connection(player))
    receiving = asyncio.create_task(receive_message(player))

    done, pending = await asyncio.wait((monitor, receiving), return_when=asyncio.FIRST_COMPLETED)
    print(done, pending)
    await asyncio.gather(player.leave_room())
    print("disconnected")


app.add_routes(routes)
