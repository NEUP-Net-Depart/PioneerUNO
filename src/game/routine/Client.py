from enum import IntEnum
from typing import Any, Union, List
from datetime import datetime

from src.game.card import Card
from src.game.player import Player


class PlayerOperationType(IntEnum):
    drawCard = 1
    putCard = 2
    go = 3
    uno = 4  # 喊uno
    notUno = 5  # 这个人没喊uno！
    unset = 0


# 拒绝套娃子类，从我做起！
class ClientOperation:
    type = PlayerOperationType.unset  # type: PlayerOperationType

    # 执行方法，传入执行者和被执行者，go没有target，uno没有target，notUno没有operator
    def perform(self, operator=None, target=None):  # type: (Player, Union[Card,Player]) -> Union[List[Card],bool,None]
        if self.type == PlayerOperationType.drawCard:
            return operator.Draw()  # type: List[Card]
        elif self.type == PlayerOperationType.putCard:
            return operator.Put(target) # type: bool
        elif self.type == PlayerOperationType.go:
            return operator.Go() # type: None
        elif self.type == PlayerOperationType.uno:
            operator.uno = True
        # 这个人真没喊uno，质疑成功，返回摸到的两张牌，质疑失败，返回false
        elif self.type == PlayerOperationType.notUno:
            if not target.uno:
                # 好，被你抓个现行，立刻摸两张牌，然后状告天下。
                target.game.current_count_of_cards_need_to_draw = 2
                return target.Draw()  # type: List[Card]
            return False


class ClientData:
    player = None  # type: Player
    operation = None  # type: ClientOperation
    # 操作对象，可以是玩家也可以是卡片。
    target = None  # type: Union[Card,Player,None]
    timestamp = None  # type: datetime
    index = 0  # 抵达服务器时，数据包按照抵达先后顺序标号。

    def __init__(self, index, player, operation, target, timestamp):
        self.index = index
        self.player = player
        self.operation = operation
        self.target = target
        self.timestamp = timestamp

    def Execute(self):  # type: (ClientData) -> Any
        return self.operation.perform(self.player, self.target)

    # A key can be a function that returns a tuple，因此比较的时候直接走就成。**Python赛高**
