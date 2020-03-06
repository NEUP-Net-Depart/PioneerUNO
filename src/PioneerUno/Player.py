import uuid


class Player:
    def __init__(self, nickname, conn=None):
        self.id = str(uuid.uuid4())
        self.conn = conn
        self.nickname = nickname
        self.room = None

    def leave_room(self):
        if self.room is not None:
            self.room.remove_player(self)
            self.room = None
