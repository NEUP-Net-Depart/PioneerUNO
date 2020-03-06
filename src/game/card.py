from enum import IntEnum


class CardColor(IntEnum):
    red = 1
    yellow = 2
    green = 3
    blue = 4
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
