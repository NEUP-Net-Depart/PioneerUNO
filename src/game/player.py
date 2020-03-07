from typing import List

from src.game.card import Card


class Player:
    cards = []  # type: List[Card]
    seat = 0  # 玩家在房间中的位置
    operation = []  # 玩家在当前回合进行的操作列表。
    game = None  # type: Game # 玩家通过game属性访问自己所处的游戏实例。

    def Put(self, card):  # type: (Card) -> None
        self.cards.remove(card)
        self.game.put(card)
        return

    def Draw(self):
        card = self.game.draw()
        self.cards.append(card)
        return card  # 将用户抽到的卡片返回给调用者

    def Go(self):
        self.game.go()  # 用户不出牌。
