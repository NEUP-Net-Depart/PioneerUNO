from enum import IntEnum


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

    def __str__(self):
        return str((self.index, self.color, self.type, self.value))

    @staticmethod
    def GenerateAllCards():
        cards = []
        index = 0
        for color in CardColor[0:3]:
            for value in range(0, 10):
                index += 1
                cards.append(Card(color, CardType.basic, value, index))
            for value in range(1, 10):
                index += 1
                cards.append(Card(color, CardType.basic, value, index))
            for card_type in CardType[1, 3]:
                index += 1
                cards.append(Card(color, card_type, 0, index))
            for i in range(0, 4):
                index += 1
                cards.append(Card(CardColor.black, CardType.drawFour, 0, index))
                index += 1
                cards.append(Card(CardColor.black, CardType.changeColor, 0, index))
