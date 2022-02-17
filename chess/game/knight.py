from typing import List

from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.square import Square


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.KNIGHT, color)

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = abs(dst.rank - src.rank)
        file_diff = abs(dst.file - src.file)
        return (rank_diff, file_diff) in [(1, 2), (2, 1)]

    def get_available_moves(self, src: Square, game_board) -> List[Move]:
        rank_and_file_steps = [(-1, -2), (-1, 2), (1, -2), (1, 2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        return super()._get_available_moves_by_steps(src, game_board, rank_and_file_steps)
