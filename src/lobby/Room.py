import asyncio
import uuid

from src.lobby.Message import player_join_event, player_leave_event, player_prepare_event, game_start_event, \
    start_countdown_event
from src.lobby.Player import Player

rooms = {}


class Room:
    def __init__(self, max_player: int):
        self.id = str(uuid.uuid4())
        self.max_player = max_player
        self.players = {}

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

    async def on_toggle_prepare_state(self, player: Player, state: bool):
        player.isPrepared = state
        await self.broadcast(player_prepare_event(
            {
                'name': player.get_name(),
                'state': player.isPrepared
            }
        ))
        if self.is_everyone_ready() and len(self.players) == self.max_player:
            await asyncio.gather(
                self.broadcast(start_countdown_event),
                self.start_count_down()
            )

    def is_everyone_ready(self):
        for player in self.players.values():
            if player.isPrepared is False:
                return False
        return True

    async def start_count_down(self):
        count = 10
        while True:
            count = count - 1
            print(count)
            await asyncio.sleep(1)
            if self.is_everyone_ready():
                if count <= 0:
                    await self.start_game()
                    break
            else:
                break

    async def start_game(self):
        print("game start!")
        await self.broadcast(game_start_event)

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


def add_room(max_player=2) -> Room:
    room = Room(max_player)
    rooms[room.id] = room
    return room
