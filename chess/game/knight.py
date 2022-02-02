from chess.game.piece import Piece
from chess.game.square import Square


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.KNIGHT, color)

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = abs(dst.rank - src.rank)
        file_diff = abs(dst.file - src.file)
        return (rank_diff, file_diff) in [(1, 2), (2, 1)]
