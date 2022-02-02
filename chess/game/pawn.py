import chess.game.board as board
from chess.game.color import Color
from chess.game.piece import Piece
from chess.game.square import Square


class Pawn(Piece):
    def __init__(self, color: Color):
        Piece.__init__(self, Piece.PAWN, color)
        if color == Color.WHITE:
            self._start_rank = board.Rank.RANK_2.value
            self._end_rank = board.Rank.RANK_8.value
            self._step = 1
        else:
            self._start_rank = board.Rank.RANK_7.value
            self._end_rank = board.Rank.RANK_1.value
            self._step = -1

    def can_move(self, src: Square, dst: Square, game_board) -> bool:
        if src.file == dst.file:
            # Move one step forward
            if src.rank + self._step == dst.rank and not game_board.has_piece(dst):
                return True
            # Move 2 steps forward from the initial position
            if (src.rank == self._start_rank
                    and dst.rank == src.rank + 2 * self._step
                    and not game_board.has_piece(src.add_rank(self._step))
                    and not game_board.has_piece(dst)):
                return True

        return self.threatens(src, dst, game_board)

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        # A pawn can capture a piece diagonally
        return (dst.rank == src.rank + self._step
                and dst.file in [src.file - 1, src.file + 1]
                and game_board.has_piece(dst))
