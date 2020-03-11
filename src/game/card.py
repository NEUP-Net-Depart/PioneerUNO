from enum import IntEnum

from typing import List


class CardColor(IntEnum):
    red = 1
    yellow = 2
    green = 3
    blue = 4
    # 注意：玩家打出黑色牌的时候，传入的参数中自动带有希望转成的颜色，效果类似于“红+4”、“绿换色”等等。
    black = 5
    unset = 0


class CardType(IntEnum):
    basic = 0
    ban = 1
    turn = 2
    drawTwo = 3
    changeColor = 4
    drawFour = 5


class Card():
    index = 0
    color = CardColor.unset
    type = CardType.basic
    value = 0

    def __init__(self, color, type, value, index):
        self.index = index
        self.color = color
        self.type = type
        self.value = value

    def __repr__(self):
        return str((self.index, self.color, self.type, self.value))

    def __str__(self):
        color_interpreter = {CardColor.red: '红', CardColor.black: '', CardColor.blue: '蓝', CardColor.green: '绿', CardColor.yellow: '黄'}
        type_interpreter = {CardType.basic: '', CardType.ban: '禁', CardType.turn: '转', CardType.drawTwo: '+2',
                            CardType.changeColor: '换色', CardType.drawFour: '+4'}
        value_str = '' if self.type != CardType.basic else str(self.value)
        return color_interpreter[self.color] + type_interpreter[self.type] + value_str

    @staticmethod
    def GenerateAllCards(start_index=1):  # type: (int) -> List[Card]
        cards = []
        index = start_index - 1
        for color in list(CardColor)[0:4]:
            for value in range(0, 10):
                index += 1
                cards.append(Card(color, CardType.basic, value, index))
            for value in range(1, 10):
                index += 1
                cards.append(Card(color, CardType.basic, value, index))
            for card_type in list(CardType)[1:4] * 2:
                index += 1
                cards.append(Card(color, card_type, 0, index))
        for i in range(0, 4):
            index += 1
            cards.append(Card(CardColor.black, CardType.drawFour, 0, index))
            index += 1
            cards.append(Card(CardColor.black, CardType.changeColor, 0, index))
        return cards
