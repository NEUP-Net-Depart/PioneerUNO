import uuid

from src.PioneerUno.Player import Player

rooms = {}


class Room:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.players = {}

    def add_player(self, player: Player):
        self.players[player.id] = player
        player.room = self

    def remove_player(self, player: Player):
        del self.players[player.id]
        if len(self.players) == 0:
            self.close()

    def close(self):
        del rooms[self.id]


def get_all_room() -> list:
    return list(rooms.keys())


def add_room() -> Room:
    room = Room()
    rooms[room.id] = room
    return room
