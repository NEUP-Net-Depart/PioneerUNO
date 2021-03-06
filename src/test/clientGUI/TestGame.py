from src.game.game import Game
from src.game.rules.GameError import GameError
from operator import attrgetter
from src.test.clientGUI.GUItester import render_player_block, render_right_area
from PyQt5.QtWidgets import *

main_game = Game(7,7)
main_game.player_list.sort(key=attrgetter('seat'))

app = QApplication([])
main_layout = QHBoxLayout()

player_block_widget = QWidget()
player_block_layout = QVBoxLayout()
right_info_widget = QWidget()
right_info_layout = QVBoxLayout()
right_info_layout.addWidget(render_right_area(main_game, player_block_layout, right_info_layout))
right_info_widget.setLayout(right_info_layout)
player_block_layout.addWidget(render_player_block(main_game, player_block_layout, right_info_layout))
player_block_widget.setLayout(player_block_layout)
main_layout.addWidget(player_block_widget)
main_layout.addWidget(right_info_widget)
main_layout_widget = QWidget()
main_layout_widget.setLayout(main_layout)
main_layout_widget.show()
main_layout_widget.setStyleSheet("font-size: 20px")
app.exec()
