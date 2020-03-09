import asyncio
import uuid

from src.game.card import Card
from src.game.game import Game
from src.lobby.Adaptor import serialize_card
from src.lobby.Message import *
from src.lobby.Player import Player

rooms = {}


async def wait_for_command(on_time_out):
    count = 0
    while count < 30:
        count = count + 1
    await on_time_out


class Room:
    def __init__(self, max_player: int, initial_card_amount: int):
        self.game = None
        self.id = str(uuid.uuid4())
        self.max_player = max_player
        self.players = {}
        self.player_role = {}
        self.role_player = {}
        self.initial_card_amount = initial_card_amount
        self.timer = None

    async def add_player(self, player: Player):
        if len(self.players) == self.max_player:
            raise Exception("room is full!")

        await self.broadcast(player_join_event(
            {
                'name': player.get_name()
            }
        ))
        self.players[player.id] = player
        player.room = self

    async def remove_player(self, player: Player):
        del self.players[player.id]
        if len(self.players) == 0:
            self.close()
        if self.game is not None:
            await self.broadcast(game_interrupted_event())
        await self.broadcast(player_leave_event(
            {
                'name': player.get_name()
            }
        ))

    async def on_toggle_prepare_state(self, player: Player, state: bool):
        player.isPrepared = state
        await self.broadcast(player_prepare_event(
            {
                'name': player.get_name(),
                'state': player.isPrepared
            }
        ))
        if self.is_everyone_ready() and len(self.players) == self.max_player:
            await asyncio.gather(
                self.broadcast(start_countdown_event),
                self.start_count_down()
            )

    def is_everyone_ready(self):
        for player in self.players.values():
            if player.isPrepared is False:
                return False
        return True

    async def start_count_down(self):
        count = 10
        while True:
            count = count - 1
            print(count)
            await asyncio.sleep(1)
            if self.is_everyone_ready():
                if count <= 0:
                    await self.start_game()
                    break
            else:
                break

    async def start_game(self):
        print("game start!")
        self.game = Game(self.max_player, self.initial_card_amount)
        for index, player in enumerate(self.players.values()):
            self.player_role[player] = self.game.player_list[index]
            self.role_player[self.game.player_list[index]] = player
        await self.broadcast(game_start_event)

    async def on_put_card(self, player: Player, card: Card):
        role = self.player_role[player]
        result = role.Put(card)
        self.cancel_timer()
        if self.timer is not None:
            self.timer.cancel()

        await self.broadcast({
            'player': player.nickname,
            'card': player_put_card_event(serialize_card(card))
        })

        if result:
            await self.broadcast(player_win_event(
                {
                    'name': player.get_name()
                }
            ))
            if len(self.game.player_list) > 1:
                await self.broadcast(game_finished_event())
                self.game = None
                self.player_role = {}
        else:
            await self.draw_card()

    async def on_skip_turn(self, player: Player):
        role = self.player_role[player]
        role.Go()
        self.cancel_timer()
        if self.timer is not None:
            self.timer.cancel()

        await asyncio.gather(
            self.broadcast(player_skip_turn_event({
                'name': player.get_name()
            })),
            self.draw_card()
        )

    async def on_cut_card(self, player: Player, card: Card):
        role = self.player_role[player]
        role.Cut(role, card)
        self.cancel_timer()
        await self.broadcast(player_cut_card_event({
            'name': player.get_name()
        }))
        await self.draw_card()

    async def on_uno(self, player: Player):
        role = self.player_role[player]
        role.Uno()
        await self.broadcast(player_uno_event({
            'name': player.get_name()
        }))

    async def on_doubt_uno(self, player: Player, data):
        role = self.player_role[player]
        target = data['target_player']
        for i in self.players:
            if target == i.get_name():
                role.DoubtUno(self.player_role[i])
                await self.broadcast(player_doubt_uno_event({
                    'from': i.get_name(),
                    'to': player.get_name()
                }))
                return

    async def draw_card(self):
        role = self.get_current_role()
        player = self.role_player[role]
        card = role.Draw()
        await asyncio.gather(
            self.broadcast(player_draw_card_event({
                'name': player.get_name()
            })),
            player.send_message(player_get_card_event({
                'card': serialize_card(card)
            }))
        )

        self.start_timer(self.on_skip_turn(role))

    def close(self):
        del rooms[self.id]

    def get_current_role(self):
        return self.game.player_list[self.game.current_player_index]

    async def broadcast(self, message):
        await asyncio.gather(
            *[
                player.send_message(message)
                for player in self.players.values()
            ]
        )

    def start_timer(self, on_time_out):
        self.timer = asyncio.create_task(wait_for_command(on_time_out))

    def cancel_timer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None


def get_all_room() -> list:
    return [
        {
            'id': i,
            'current_player': len(i.players),
            'max_player': i.max_player
        }
        for i in rooms
    ]


def add_room(max_player=2) -> Room:
    room = Room(max_player)
    rooms[room.id] = room
    return room
