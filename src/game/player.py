from typing import List

from src.game.card import Card


class Player:
    cards = []  # type: List[Card]
    seat = 0 # 玩家在房间中的位置
