from chess.game.piece import Piece
from chess.game.square import Square


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.BISHOP, color)

    def can_move(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = dst.rank - src.rank
        file_diff = dst.file - src.file
        if abs(rank_diff) != abs(file_diff):
            return False
        rank_step = rank_diff // abs(rank_diff)
        file_step = file_diff // abs(file_diff)
        square = Square(file=src.file + file_step, rank=src.rank + rank_step)

        # Check there are no pieces between the source and the destination.
        while square != dst:
            if game_board.has_piece(square):
                return False
            square = Square(file=square.file + file_step, rank=square.rank + rank_step)
        return True
