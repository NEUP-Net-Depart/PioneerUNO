import asyncio
import uuid

from src.PioneerUno.Message import player_join_event, player_leave_event
from src.PioneerUno.Player import Player

rooms = {}


class Room:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.players = {}

    async def add_player(self, player: Player):
        await self.broadcast(player_join_event(
            {
                'name': player.get_name()
            }
        ))
        self.players[player.id] = player
        player.room = self

    async def remove_player(self, player: Player):
        del self.players[player.id]
        if len(self.players) == 0:
            self.close()
        await self.broadcast(player_leave_event(
            {
                'name': player.get_name()
            }
        ))

    def close(self):
        del rooms[self.id]

    async def broadcast(self, message):
        await asyncio.gather(
            *[
                player.send_message(message)
                for player in self.players.values()
            ]
        )


def get_all_room() -> list:
    return list(rooms.keys())


def add_room() -> Room:
    room = Room()
    rooms[room.id] = room
    return room
