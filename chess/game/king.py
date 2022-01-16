from chess.game.piece import Piece
from chess.game.square import Square


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.KING, color)

    def can_move(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = abs(dst.rank - src.rank)
        file_diff = abs(dst.file - src.file)
        return rank_diff == 0 and file_diff == 1 or file_diff == 0 and rank_diff == 1
