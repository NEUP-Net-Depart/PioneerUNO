from src.game.card import Card, CardColor, CardType
from random import shuffle


class Game:
    player_list = []
    card_pool = []  # 自动洗牌。
    current_player_index = 0  # 现在应该进行操作的玩家
    current_take_turns_positive = True  # 游戏正向进行，下一个出牌的玩家编号应该为(当前编号+1或2)%人数。
    current_count_of_cards_need_to_draw = 0  # 加牌叠加的数量
    current_card = None  # 当前状态位于牌堆顶的卡片

    def _next_player(self, value=1):
        if self.current_take_turns_positive:
            self.current_player_index = (self.current_player_index + value) % len(self.player_list)
        else:
            self.current_player_index = (self.current_player_index - value) % len(self.player_list)

    def shuffle(self):
        self.card_pool = shuffle(Card.GenerateAllCards())

    # player methods
    # put是一个原子操作，玩家出牌后游戏状态立即改变，他不能继续出牌。
    def put(self, card):  # type: (Card) -> None
        self.current_card = card
        # 接下来，根据玩家出牌的不同而判断不同的逻辑。
        if card.type == CardType.ban:
            self._next_player(2)
            return
        elif card.type == CardType.turn:
            self.current_take_turns_positive = not self.current_take_turns_positive
        elif card.type == CardType.drawTwo:
            self.current_count_of_cards_need_to_draw += 2
        elif card.type == CardType.drawFour:
            self.current_count_of_cards_need_to_draw += 4
        # 对于ChangeColor和基本牌，我们什么也不需要做。
        self._next_player()
