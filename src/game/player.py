from typing import List

from src.game.card import Card
from src.game.game import Game
from src.game.rules.Validator import Validator


class Player:
    validator = None  # type: Validator # 玩家的监督者，坚定不移的铁面判官Validator!
    cards = []  # type: List[Card]
    seat = 0  # 玩家在房间中的位置
    operation_count = 0  # 玩家在当前回合进行的操作数量
    game = None  # type: Game # 玩家通过game属性访问自己所处的游戏实例。
    uno = False  # type: bool # 玩家喊uno了吗？玩家的uno状态会在玩家准备出牌前置为false。玩家设计上可以随时uno，但客户端应该保证他尽量在他自己的回合uno。

    def __init__(self, game, seat):
        self.game = game
        self.seat = seat
        self.validator = Validator(game, self)

    def _remove_card(self, card_index):
        for card in self.cards:
            if card.index == card_index:
                del card
                return

    # Put方法为用户的一般出牌，切牌请走Cut方法。
    def Put(self, card):  # type: (Card) -> bool # 返回获胜与否。
        self.validator.canPut(card)
        self.uno = False  # 玩家出牌之前，它uno的状态便不复存在，**这里不存在任何设计问题，写这段代码的人是Neboer，欢迎与我对线。**
        self._remove_card(card.index)
        self.game.put(card)
        self.operation_count = 0
        if len(self.cards) == 0:
            # 恭喜你，你赢了！
            self.game.win(self)
            return True
        return False

    # 这个是玩家的切牌。
    def Cut(self, card):  # type: (Player) -> None
        self.validator.canCut(card)
        self._remove_card(card.index)
        self.game.cut(self, card)
        return

    def Draw(self):  # type: () -> List[Card]
        self.validator.canDraw()
        cards = self.game.draw()
        self.cards += cards
        self.operation_count += 1
        return cards  # 将用户抽到的卡片返回给调用者

    def Go(self):  # type: () -> None
        self.game.go()  # 用户不出牌。
        self.operation_count = 0
        return

    def Uno(self):  # type: () -> None
        self.validator.canUno()
        self.uno = True
        return

    def DoubtUno(self, target_player):  # type: (Player)->bool
        self.validator.canDoubtUno(target_player)
        if not target_player.uno and len(target_player.cards) == 1:
            self.game.punishUno(target_player)
            # 质疑成功，返回True
            return True
        else:
            return False
