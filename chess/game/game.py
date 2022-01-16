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

    def move(self, src: Square, dst: Square) -> bool:
        piece = self._board.get_piece(src)
        target_piece = self._board.get_piece(dst)

        if piece is None:
            return False
        if piece.color() != self._turn:
            return False
        if target_piece is not None and target_piece.color() == self._turn:
            return False
        if not piece.can_move(src, dst, self._board):
            return False

        self._board.remove_piece(src)
        self._board.set_piece(dst, piece)
        self._turn = Color.WHITE if self._turn == Color.BLACK else Color.BLACK

        return True
