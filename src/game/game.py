from src.game.card import Card, CardColor, CardType
from random import shuffle
from src.game.player import Player


class Game:
    player_list = []
    card_pool = []  # 自动洗牌。
    shuffle_times = 0  # 洗过几次牌？在一开始应该算一次，这个值用来生成牌index。
    current_player_index = 0  # 现在应该进行操作的玩家
    current_take_turns_positive = True  # 游戏正向进行，下一个出牌的玩家编号应该为(当前编号+1或2)%人数。
    current_count_of_cards_need_to_draw = 0  # 加牌叠加的数量
    current_card = None  # 当前状态位于牌堆顶的卡片

    # 牌总是从后向前pop的，也就是优先弹出index较大的。如果牌不够了，就先pop全部然后洗牌再pop。
    def _pop_cards(self, number):
        if len(self.card_pool) < number:
            part_one = self.card_pool
            self._shuffle()
            part_two = self.card_pool[-(number - len(part_one)):]
            del self.card_pool[-(number - len(part_one)):]
            return part_one + part_two
        elif len(self.card_pool) == number:
            part = self.card_pool
            self._shuffle()
            return part
        else:
            part = self.card_pool[-number:]
            del self.card_pool[-number:]
            return part

    # 创建一个游戏。
    def __init__(self, player_count, draw_cards):  # 传入初始玩家应该拥有手牌的数量
        self.player_list = [Player(self, seat) for seat in range(1, player_count + 1)]
        self._shuffle()
        for player in self.player_list:
            player.cards = self._pop_cards(draw_cards)  # 发牌
        self.current_player_index = 1
        self.current_take_turns_positive = True
        self.current_count_of_cards_need_to_draw = 1

    def _next_player(self, value=1):
        if self.current_take_turns_positive:
            self.current_player_index = (self.current_player_index + value) % len(self.player_list)
        else:
            self.current_player_index = (self.current_player_index - value) % len(self.player_list)

    def _shuffle(self):
        self.card_pool = shuffle(Card.GenerateAllCards(108 * self.shuffle_times + 1))
        self.shuffle_times += 1

    # player methods
    # put是一个原子操作，玩家出牌后游戏状态立即改变，他不能继续出牌。put是玩家正常出牌的方法。
    def put(self, card):  # type: (Card) -> None
        self.current_card = card
        # 接下来，根据玩家出牌的不同而判断不同的逻辑。
        if card.type == CardType.ban:
            self._next_player(2)
            return
        elif card.type == CardType.turn:
            self.current_take_turns_positive = not self.current_take_turns_positive
        elif card.type == CardType.drawTwo:
            self.current_count_of_cards_need_to_draw += 2 if self.current_count_of_cards_need_to_draw != 1 else 1
        elif card.type == CardType.drawFour:
            self.current_count_of_cards_need_to_draw += 4 if self.current_count_of_cards_need_to_draw != 1 else 3
        # 对于ChangeColor和基本牌，我们什么也不需要做。
        self._next_player()
        return

    def draw(self):
        prepare_cards = self._pop_cards(self.current_count_of_cards_need_to_draw)
        self.current_count_of_cards_need_to_draw = 1  # 用户摸牌后，牌局总需要摸牌的数量归1
        # 玩家摸牌后，对局不继续进行，等待他的下一步操作。
        return prepare_cards

    def go(self):
        self._next_player()

    # cut是玩家切牌。玩家切牌后，游戏就从玩家处继续进行。
    def cut(self, player, card):  # type: (Player, Card) -> None
        # 玩家切牌的逻辑也很简单，只需要把“出牌”的发生地改成切牌玩家的seat然后再出牌就可以。
        self.current_player_index = player.seat
        self.put(card)
        return
