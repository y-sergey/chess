from chess.game.piece import Piece
from chess.game.square import Square


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.QUEEN, color)

    def can_move(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = dst.rank - src.rank
        file_diff = dst.file - src.file
        same_line = rank_diff == 0 or file_diff == 0 or (abs(file_diff) == abs(rank_diff))
        if not same_line:
            return False
        return not game_board.has_pieces_between(src, dst)
