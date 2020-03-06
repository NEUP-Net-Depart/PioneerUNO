import uuid


class Player:
    def __init__(self, nickname, conn=None):
        self.id = uuid.uuid4()
        self.conn = conn
        self.nickname = nickname
