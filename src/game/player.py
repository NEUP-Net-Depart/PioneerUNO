from typing import List

from src.game.card import Card


class Player:
    cards = []  # type: List[Card]
    seat = 0  # 玩家在房间中的位置
    operation_count = 0  # 玩家在当前回合进行的操作数量
    game = None  # type: Game # 玩家通过game属性访问自己所处的游戏实例。

    def __init__(self, game, seat):
        self.game = game
        self.seat = seat

    def _remove_card(self, card_index):
        for card in self.cards:
            if card.index == card_index:
                del card
                return

    # Put方法为用户的一般出牌，切牌请走Cut方法。
    def Put(self, card):  # type: (Card) -> bool
        self._remove_card(card.index)
        self.game.put(card)
        self.operation_count = 0
        if len(self.cards) == 0:
            # 恭喜你，你赢了！
            self.game.win(self)
            return True
        return False

    # 这个是玩家的切牌。
    def Cut(self, card):
        self._remove_card(card.index)
        self.game.cut(self, card)
        return

    def Draw(self):
        card = self.game.draw()
        self.cards.append(card)
        self.operation_count += 1
        return card  # 将用户抽到的卡片返回给调用者

    def Go(self):
        self.game.go()  # 用户不出牌。
        self.operation_count = 0
        return
