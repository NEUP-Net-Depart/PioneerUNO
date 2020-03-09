from typing import Any, Union
from .Client import PlayerOperationType

from src.game.card import Card
from src.game.player import Player


class ServerData:
    Operator = None  # type: Player
    OperationType = None  # type: PlayerOperationType
    OperationTarget = None  # type: Union[Card, None, Player]
