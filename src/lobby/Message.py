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


game_interrupted_event = Message(130)
game_finished_event = Message(120)
start_countdown_event = Message(110)
game_start_event = Message(100)

player_win_event = Message(10)
player_cut_card_event = Message(9)
player_get_card_event = Message(8)
player_skip_turn_event = Message(7)
player_put_card_event = Message(6)
player_draw_card_event = Message(5)
player_cancel_prepare_event = Message(4)
player_prepare_event = Message(3)
player_leave_event = Message(2)
player_join_event = Message(1)

missing_parameters_error = respond_json(-1, "missing parameters")
unknown_command = respond_json(-2, "unknown command")
unknown_uuid_error = respond_json(-3, "unknown player")
unknown_room_id = respond_json(-4, "unknown room id")
room_is_full = respond_json(-5, "room is full")
already_in_room = respond_json(-6, "already_in_room")
