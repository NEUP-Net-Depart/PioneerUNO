import uuid

from src.PioneerUno.Player import Player


class Room:
    def __init__(self):
        self.id = uuid.uuid4()
        self.players = {}

    def add_player(self, player: Player):
        self.players[player.id] = player
