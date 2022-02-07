from typing import List

from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.square import Square


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.ROOK, color)

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = dst.rank - src.rank
        file_diff = dst.file - src.file
        same_line = rank_diff == 0 or file_diff == 0
        return same_line and not game_board.has_pieces_between(src, dst)

    def get_valid_moves(self, src: Square, game_board) -> List[Move]:
        rank_and_file_steps = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        return super()._search_valid_moves_by_steps(src, game_board, rank_and_file_steps)
