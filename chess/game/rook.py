from chess.game.piece import Piece
from chess.game.square import Square


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.ROOK, color)

    def can_move(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = dst.rank - src.rank
        file_diff = dst.file - src.file
        if not (rank_diff == 0 or file_diff == 0):
            return False
        return not game_board.has_pieces_between(src, dst)

