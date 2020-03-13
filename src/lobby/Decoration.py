from functools import wraps

from src.game.rules.GameError import *
from src.lobby.Message import *


def catch_put_exceptions(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            return await function(args, kwargs)
        except FirstCardIsFunctionalCardError:
            return invalid_first_card
        except PlayerPutNormalCardWhenUnderAdmonish:
            return invalid_placement_during_admonish
        except PlayerLastCardIsFunctionalCardError:
            return last_card_is_functional_card
        except PlayerPutCardNotCorrectWithLastCardError:
            return invalid_placement
        except PlayerPutCardsNotAtHisTurnError:
            return invalid_turn
        except PlayerNoSuchCardError:
            return no_such_card
        except PlayerPutBlackCardError:
            return put_black_card

    return wrapper
