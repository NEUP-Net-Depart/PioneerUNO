class Message:
    def __init__(self, status: int, data=None):
        self.status = status
        self.data = data

    def __call__(self, *args, **kwargs):
        if len(args) > 0:
            self.data = args[0]
        return self

    def json(self):
        return {
            'status': self.status,
            'data': self.data
        }


def respond_json(status: int, data=None):
    return Message(status, data).json()


def respond_success(data=None):
    return respond_json(0, data)


player_leave_event = Message(2)
player_join_event = Message(1)

missing_parameters_error = respond_json(-1, "missing parameters")
unknown_command = respond_json(-2, "unknown command")
unknown_uuid_error = respond_json(-3, "unknown player")
unknown_room_id = respond_json(-4, "unknown room id")
