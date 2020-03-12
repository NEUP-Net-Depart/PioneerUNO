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


class PlayerPassWithoutAction(GameError):
    pass


class PlayerDrewCardMultiTimesError(GameError):
    pass


# 按照先锋规则，玩家不应该切自己刚刚出的牌。
class PlayerCutItsOwnCardError(GameError):
    pass


# 按照先锋规则，被禁玩家不能切禁自己的禁牌。
class BannedPlayerCutBanCardError(GameError):
    pass
