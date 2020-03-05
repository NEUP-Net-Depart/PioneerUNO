import uuid

players = {}


class Player:
    def __init__(self, conn, nickname):
        self.id = uuid.uuid4()
        self.conn = conn
        self.nickname = nickname
