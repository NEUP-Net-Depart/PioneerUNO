
from src.game.card import Card, CardType, CardColor
from src.game.rules.GameError import *


# Validator是和Game中的玩家对象一一对应的关系，每个玩家都有自己的校验器，方法和玩家对象的方法基本相同，用来在玩家进行不同操作之前校验其是否可以操作。
# 你指尖跃动的电光，是我此生不变的信仰！
class Validator:
    game = None
    player = None

    def __init__(self, game_obj, player_obj):
        self.game = game_obj
        self.player = player_obj

    # 玩家是否拥有他出的那张牌？
    def _have_card_check(self, card):
        if card.index not in [player_card.index for player_card in self.player.cards]:
            raise PlayerNoSuchCardError

    # 玩家是否为下一个应该出牌的人？
    def _player_must_next(self):
        if self.game.current_player_seat != self.player.seat:
            raise PlayerPutCardsNotAtHisTurnError

    @staticmethod
    def _cannot_put_black_card(card):
        if card.color == CardColor.black:
            raise PlayerPutBlackCardError

    # 对当前玩家Validator应用检验，返回该玩家是否需要UNO。
    def needUNO(self):
        return len(self.player.cards) == 1

    # 玩家是否可以切牌？
    def canCut(self, card):  # type: (Card) -> None
        self._have_card_check(card)
        # 黑色牌（加四牌和换色牌）不能切
        if card.type == CardType.drawFour or card.type == CardType.changeColor:
            raise PlayerPutBlackCardError
        # 卡片必须完全一致才能切牌。
        elif card.color == self.game.current_card.color and card.type == self.game.current_card.type and card.value == self.game.current_card.value:
            return
        else:
            raise PlayerCutCardsNotEqualToCurrentError

    # 玩家是否可以出牌？
    def canPut(self, card):  # type: (Card) -> None
        self._player_must_next()
        self._have_card_check(card)
        self._cannot_put_black_card(card)
        current_card = self.game.current_card
        # 黑色牌可以随意出。
        # 想到了：黑牌不可以随意出。如果玩家还有需要多模的牌，他要么出"+2"要么出"+4"。
        if self.game.current_count_of_cards_need_to_draw > 1:
            # 如果玩家正在被“+2”或“+4”，他的出牌只能局限于加牌，他不能出任何其他的牌。
            if card.type != CardType.drawTwo or card.type != CardType.drawFour:
                raise PlayerPutNormalCardWhenUnderAdmonish
        # 如果玩家的此次出牌是他的最后一张牌，那么这张牌不能为功能牌。
        if len(self.player.cards) == 1 and card.type != CardType.basic:
            raise PlayerLastCardIsFunctionalCardError
        # 非黑色牌，要么和上一张牌颜色相同，要么都为功能牌且type相同，要么都为基本牌且value相同。
        if card.type == CardType.drawFour or card.type == CardType.changeColor:
            return
        elif card.color == current_card.color:
            return
        elif card.type in [CardType.drawTwo, CardType.turn, CardType.ban]:
            if card.type == current_card.type:
                return
            else:
                raise PlayerPutCardNotCorrectWithLastCardError
        elif card.type == CardType.basic and current_card.type == CardType.basic:
            if card.value == current_card.value:
                return
            else:
                raise PlayerPutCardNotCorrectWithLastCardError

    # 玩家是否可以摸牌？似乎没啥限制，想摸就摸吧，只要轮到你了就可以。
    def canDraw(self):  # type: () -> None
        self._player_must_next()

    def canUno(self):  # type: () -> None
        if len(self.player.cards) > 1:
            raise PlayerUnoWithManyCardsError

    def canDoubtUno(self, player):  # type: (Player) -> None
        if player not in self.game.player_list:
            raise DoubtTargetPlayerNotInPlayerListError
