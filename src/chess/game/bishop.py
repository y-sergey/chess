from typing import List

from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.square import Square


class Bishop(Piece):
    _MOVE_STEPS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def __init__(self, color):
        Piece.__init__(self, Piece.BISHOP, color, material_value=3)

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = dst.rank - src.rank
        file_diff = dst.file - src.file
        same_diagonal = abs(rank_diff) == abs(file_diff)
        return same_diagonal and not game_board.has_pieces_between(src, dst)

    def get_available_moves(self, src: Square, game_board) -> List[Move]:
        return super()._search_available_moves_by_steps(src, game_board, Bishop._MOVE_STEPS)
