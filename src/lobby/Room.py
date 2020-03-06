import asyncio
import uuid
from threading import Timer

from src.lobby.Message import player_join_event, player_leave_event, player_prepare_event
from src.lobby.Player import Player

rooms = {}


class Room:
    def __init__(self, max_player: int):
        self.timer = Timer(1.0, self.__on_count_down)
        self.id = str(uuid.uuid4())
        self.max_player = max_player
        self.players = {}
        self.prepare = 0

    async def add_player(self, player: Player):
        if len(self.players) == self.max_player:
            raise Exception("room is full!")

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

    async def on_prepare(self, player: Player, state: bool):
        await self.broadcast(player_prepare_event({
            {
                'name': player.get_name()
            }
        }))

        for player in self.players:
            if player.isPrepared is False:
                return

    def start_count_down(self):
        pass

    def __on_count_down(self):
        pass

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
