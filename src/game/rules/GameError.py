# 游戏错误
class GameError(Exception):
    pass


class PlayerNoSuchCardError(GameError):
    pass


class PlayerPutCardsNotAtHisTurnError(GameError):
    pass


class PlayerPutBlackCardError(GameError):
    pass


class PlayerCutBlackCardError(GameError):
    pass

class PlayerCutCardsNotEqualToCurrentError(GameError):
    pass