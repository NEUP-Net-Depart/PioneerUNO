from src.game.game import Game, Player  #
from src.game.card import Card  #
from PyQt5.QtWidgets import *


def _update_player_block(game_obj, mainLayout):
    newWidgeter = render_player_block(game_obj, mainLayout)
    widget_need_update = mainLayout.itemAt(0).widget()
    widget_need_update.close()
    mainLayout.replaceWidget(widget_need_update, newWidgeter)


def generate_put_function(player, card, mainLayout):
    def putCard():
        player.Put(card)
        _update_player_block(player.game, mainLayout)

    return putCard


def generate_draw_function(game, mainLayout):
    def drawCard():
        player = game.current_player()
        player.Draw()
        _update_player_block(game, mainLayout)

    return drawCard


def render_player_block(game, mainLayout):  # type: (Game, QVBoxLayout) -> QWidget
    all_players_metas_block_layout = QVBoxLayout()
    for player in game.player_list:
        player_meta_bar_layout = QHBoxLayout()
        player_seat_label = QLabel(str(player.seat))
        if game.current_player_seat == player.seat:
            player_seat_label.setStyleSheet("border: 1px solid red;")
        player_card_button_list = []
        for card in player.cards:
            card_btn = QPushButton(str(card))
            card_btn.clicked.connect(generate_put_function(player, card, mainLayout))
            player_card_button_list.append(card_btn)
        for widget in [player_seat_label] + player_card_button_list:
            player_meta_bar_layout.addWidget(widget)
        player_meta_bar = QWidget()
        player_meta_bar.setLayout(player_meta_bar_layout)
        all_players_metas_block_layout.addWidget(player_meta_bar)
    players_meta_block_widget = QWidget()
    players_meta_block_widget.setLayout(all_players_metas_block_layout)
    return players_meta_block_widget


def render_right_area(game, mainLayout):
    largest_layout = QVBoxLayout()
    draw_card_btn = QPushButton("摸牌")
    draw_card_btn.clicked.connect(generate_draw_function(game, mainLayout))
    largest_layout.addWidget(draw_card_btn)
    right_area_widget = QWidget()
    right_area_widget.setLayout(largest_layout)
    return right_area_widget
