import uuid
from time import time

from src.game.card import Card
from src.lobby.Message import player_chat_event


class Player:
    def __init__(self, nickname, conn=None):
        self.id = str(uuid.uuid4())
        self.conn = conn
        self.nickname = nickname
        self.room = None
        self.isPrepared = False
        self.last_time_active = time()

    def get_name(self):
        return f'{self.nickname}@{self.id[:4]}'

    async def leave_room(self):
        if self.room is not None:
            await self.room.remove_player(self)
            self.room = None

    async def send_message(self, message):
        await self.conn.send_json(message.json())

    async def toggle_preparing_state(self, state: bool):
        self.isPrepared = state
        if self.room is not None:
            await self.room.on_toggle_prepare_state(self, state)

    async def put_card(self, card: Card):
        self.room.on_put_card(self, card)

    async def skip_turn(self):
        self.room.on_skip_turn(self)

    async def cut_card(self, card: Card):
        self.room.on_cut_card(self, card)

    async def uno(self):
        self.room.on_uno(self)

    async def chat(self, message):
        self.room.broadcast(player_chat_event({
            'message': message,
            'speaker': self.get_name()
        }))
