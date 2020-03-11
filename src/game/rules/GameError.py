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


class PlayerPutCardNotCorrectWithLastCardError(GameError):
    pass


# 玩家在被+2+4的时候出非加牌
class PlayerPutNormalCardWhenUnderAdmonish(GameError):
    pass


class PlayerLastCardIsFunctionalCardError(GameError):
    pass


class PlayerUnoWithManyCardsError(GameError):
    pass


class DoubtTargetPlayerNotInPlayerListError(GameError):
    pass


class FirstCardIsFunctionalCardError(GameError):
    pass
