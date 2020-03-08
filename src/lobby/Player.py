import uuid

from src.game.card import Card


class Player:
    def __init__(self, nickname, conn=None):
        self.id = str(uuid.uuid4())
        self.conn = conn
        self.nickname = nickname
        self.room = None
        self.isPrepared = False

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
