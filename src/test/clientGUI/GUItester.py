from src.game.game import Game, Player  #
from src.game.card import Card, CardColor  #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import types


# 对函数进行深度拷贝的方法，pull from stackoverflow
def copy_func(f, name=None):
    '''
    return a function with same code, globals, defaults, closure, and
    name (or provide a new name)
    '''
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
                            f.__defaults__, f.__closure__)
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    return fn


def _update_player_block(game_obj, player_meta_block_layout, right_meta_layout):
    old_player_widget = player_meta_block_layout.itemAt(0).widget()
    old_player_widget.close()
    player_meta_block_layout.replaceWidget(old_player_widget,
                                           render_player_block(game_obj, player_meta_block_layout, right_meta_layout))
    old_game_metainfo_widget = right_meta_layout.itemAt(0).widget()
    old_game_metainfo_widget.close()
    right_meta_layout.replaceWidget(old_game_metainfo_widget,
                                    render_right_area(game_obj, player_meta_block_layout, right_meta_layout))


def choose_color_widget(card):
    dialog = QDialog()
    dialog_layout = QHBoxLayout()
    four_color = list(CardColor)[:4]

    def changer_generator(to_color):
        def changer():
            card.color = to_color
            dialog.close()

        return changer

    for one_color in four_color:
        color_button = QPushButton(one_color.toStr())
        color_button.clicked.connect(changer_generator(one_color))
        dialog_layout.addWidget(color_button)
    dialog.setLayout(dialog_layout)
    return dialog


def generate_put_function(player, card, player_info_block_layout, right_meta_layout):
    def putCard():
        if player.game.current_player_seat == player.seat:
            if card.color == CardColor.black:
                choose_color_widget(card).exec()
            player.Put(card)
        else:
            player.Cut(card)
        _update_player_block(player.game, player_info_block_layout, right_meta_layout)

    return putCard


def generate_draw_function(game, player_info_block_layout, right_meta_layout):
    def drawCard():
        player = game.current_player()
        player.Draw()
        _update_player_block(game, player_info_block_layout, right_meta_layout)

    return drawCard


def generate_go_function(game, player_info_block_layout, right_meta_layout):
    def go():
        player = game.current_player()
        player.Go()
        _update_player_block(game, player_info_block_layout, right_meta_layout)

    return go


def render_player_block(game, player_info_block_layout, right_meta_layout):
    all_players_metas_block_layout = QVBoxLayout()
    for player in game.player_list:
        player_meta_bar_layout = QHBoxLayout()
        player_meta_bar_layout.setAlignment(Qt.AlignLeft)
        player_seat_label = QLabel(str(player.seat))
        if game.current_player_seat == player.seat:
            player_seat_label.setStyleSheet("border: 1px solid red;")
        player_card_button_list = []
        for card in player.cards:
            card_btn = QPushButton(str(card))
            card_btn.clicked.connect(generate_put_function(player, card, player_info_block_layout, right_meta_layout))
            player_card_button_list.append(card_btn)
        for widget in [player_seat_label] + player_card_button_list:
            player_meta_bar_layout.addWidget(widget)
        player_meta_bar = QWidget()
        player_meta_bar.setLayout(player_meta_bar_layout)
        all_players_metas_block_layout.addWidget(player_meta_bar)
    players_meta_block_widget = QWidget()
    players_meta_block_widget.setLayout(all_players_metas_block_layout)
    players_meta_block_widget.setStyleSheet('''
    QPushButton { max-width: 50px; float: left }
    QLabel {max-width: 10px}
    ''')
    return players_meta_block_widget


def render_right_area(game, player_block_layout, right_info_layout):
    self_right_meta_block = QVBoxLayout()
    self_right_meta_block.addWidget(QLabel(str(game.current_card)))
    draw_card_btn = QPushButton("摸牌")
    draw_card_btn.clicked.connect(generate_draw_function(game, player_block_layout, right_info_layout))
    self_right_meta_block.addWidget(draw_card_btn)
    go_btn = QPushButton("过")
    go_btn.clicked.connect(generate_go_function(game, player_block_layout, right_info_layout))
    self_right_meta_block.addWidget(go_btn)
    right_area_widget = QWidget()
    right_area_widget.setLayout(self_right_meta_block)
    return right_area_widget
