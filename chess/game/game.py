from chess.game.board import Board
from chess.game.color import Color
from chess.game.square import Square


class Game:
    def __init__(self):
        self._board = Board()
        self._turn = Color.WHITE

    def board(self):
        return self._board

    def current_player(self):
        return self._turn

    def move(self, pos_from: Square, pos_to: Square) -> bool:
        piece = self._board.get_piece(pos_from)
        target_piece = self._board.get_piece(pos_to)

        if piece is None:
            return False
        if piece.color() != self._turn:
            return False
        if target_piece is not None and target_piece.color() == self._turn:
            return False

        self._board.remove_piece(pos_from)
        self._board.set_piece(pos_to, piece)
        self._turn = Color.WHITE if self._turn == Color.BLACK else Color.BLACK

        return True
