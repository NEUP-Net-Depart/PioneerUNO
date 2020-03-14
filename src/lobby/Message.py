class Message:
    def __init__(self, status: int, request_id=None, data=None, ):
        self.status = status
        self.data = data
        self.request_id = request_id

    def __call__(self, *args, **kwargs):
        if len(args) > 0:
            self.data = args[0]
        return self

    def json(self):
        return {
            'status': self.status,
            'data': self.data
        }


def respond_json(status: int, data=None, request_id=None):
    return Message(status, request_id, {
        'msg': data,
    }).json()


def respond_success(data=None):
    return respond_json(0, data)


game_interrupted_event = Message(103)
game_finished_event = Message(102)
start_countdown_event = Message(101)
game_start_event = Message(100)

player_chat_event = Message(13)
player_doubt_uno_event = Message(12)
player_uno_event = Message(11)
player_win_event = Message(10)
player_cut_card_event = Message(9)
player_get_card_event = Message(8)
player_skip_turn_event = Message(7)
player_put_card_event = Message(6)
player_draw_card_event = Message(5)
player_cancel_preparation_event = Message(4)
player_prepare_event = Message(3)
player_leave_event = Message(2)
player_join_event = Message(1)

missing_parameters_error = respond_json(-1, "missing parameters")
unknown_command = respond_json(-2, "unknown command")
unknown_uuid_error = respond_json(-3, "unknown player")
unknown_room_id = respond_json(-4, "unknown room id")
room_is_full = respond_json(-5, "room is full")
already_in_room = respond_json(-6, "already_in_room")
no_such_card = respond_json(-7, "no such card")
invalid_turn = respond_json(-8, "invalid turn")
put_black_card = respond_json(-9, "put black card error")
cut_black_card = respond_json(-10, "cut black card error")
cut_card_not_equal = respond_json(-11, "cut card not equal")
invalid_placement = respond_json(-12, "card number is not equal to last card")
invalid_placement_during_admonish = respond_json(-13, "invalid placement during admonish")
last_card_is_functional_card = respond_json(-14, "last card is functional card")
invalid_uno = respond_json(-15, "invalid uno")
invalid_first_card = respond_json(-16, "invalid first card")
