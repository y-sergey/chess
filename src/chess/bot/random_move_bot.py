import random

from chess.game.color import Color
from chess.game.game import Game
from chess.game.move import Move


class RandomMoveBot:

    def __init__(self, color: Color, game: Game):
        self._color = color
        self._game = game

    def move(self) -> Move:
        valid_moves = self._game.get_available_moves(self._color)
        return random.choice(valid_moves)

    def color(self) -> Color:
        return self._color
