from typing import List

from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.piece_table_values import KNIGHT_PST
from chess.game.square import Square


class Knight(Piece):
    _MOVE_STEPS = [(-1, -2), (-1, 2), (1, -2), (1, 2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def __init__(self, color):
        Piece.__init__(
            self,
            Piece.KNIGHT,
            color, material_value=320,
            piece_table_value=KNIGHT_PST)

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = abs(dst.rank - src.rank)
        file_diff = abs(dst.file - src.file)
        return (rank_diff == 1 and file_diff == 2) or (rank_diff == 1 and file_diff == 2)

    def get_available_moves(self, src: Square, game_board) -> List[Move]:
        return super()._get_available_moves_by_steps(src, game_board, Knight._MOVE_STEPS)
