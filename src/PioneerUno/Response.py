def respond_json(status: int, data=None):
    return {
        'status': status,
        'data': data
    }


def respond_success(data=None):
    return respond_json(0, data)


missing_parameters_error = respond_json(-1, "missing parameters")
unknown_command = respond_json(-2, "unknown_command")
unknown_uuid_error = respond_json(-3, "unknow_player")
