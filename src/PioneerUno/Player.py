import uuid


class Player:
    def __init__(self, nickname, conn=None):
        self.id = str(uuid.uuid4())
        self.conn = conn
        self.nickname = nickname
        self.room = None

    def get_name(self):
        return f'{self.nickname}@{self.id[:4]}'

    async def leave_room(self):
        if self.room is not None:
            await self.room.remove_player(self)
            self.room = None

    async def send_message(self, message):
        await self.conn.send_json(message.json())
