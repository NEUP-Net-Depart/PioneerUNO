from src.game.game import Game
from src.game.card import Card, CardType, CardColor
from src.game.player import Player
from src.game.rules.GameError import *


# Validator是和Game中的玩家对象一一对应的关系，每个玩家都有自己的校验器，方法和玩家对象的方法基本相同，用来在玩家进行不同操作之前校验其是否可以操作。
# 你指尖跃动的电光，是我此生不变的信仰！
class Validator:
    game = None  # type: Game
    player = None  # type: Player

    def __init__(self, game_obj, player_obj):
        self.game = game_obj
        self.player = player_obj

    # 玩家是否拥有他出的那张牌？
    def _have_card_check(self, card):
        if card.index not in [player_card.index for player_card in self.player.cards]:
            raise PlayerNoSuchCardError

    # 玩家是否为下一个应该出牌的人？
    def _player_must_next(self):
        if self.game.current_player_index != self.player.seat:
            raise PlayerPutCardsNotAtHisTurnError

    def _cannot_put_black_card(self, card):
        if card.color == CardColor.black:
            raise PlayerPutBlackCardError

    # 玩家是否可以切牌？
    def canCut(self, card):
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
    def canPut(self, card):
        self._player_must_next()
        self._have_card_check(card)
        self._cannot_put_black_card(card)
        current_card = self.game.current_card
        # 黑色牌可以随意出。
        # 非黑色牌，要么和上一张牌颜色相同，要么都为基本牌且value相同，要么都为功能牌且type相同。
        if card.type == CardType.drawFour or card.type == CardType.changeColor:
            return
        elif card.color == current_card.color:
            return
        elif card.type in [CardType.drawTwo, CardType.turn, CardType.]
        if card.color == current_card.color or (card.type == CardType.basic and current_card.type == CardType.basic and card.value == current_card.value) or ()
