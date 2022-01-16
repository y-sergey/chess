from chess.game.bishop import Bishop
from chess.game.color import Color
from chess.game.king import King
from chess.game.knight import Knight
from chess.game.pawn import Pawn
from chess.game.piece import Piece
from chess.game.queen import Queen
from chess.game.rook import Rook
from chess.game.square import Square

from enum import Enum
from enum import unique


@unique
class Rank(Enum):
    RANK_1 = 0
    RANK_2 = 1
    RANK_3 = 2
    RANK_4 = 3
    RANK_5 = 4
    RANK_6 = 5
    RANK_7 = 6
    RANK_8 = 7


@unique
class File(Enum):
    FILE_A = 0
    FILE_H = 7


class Board:
    NUM_RANKS = 8
    NUM_FILES = 8

    def __init__(self):
        self._pieces = [[None for _ in range(8)] for _ in range(8)]
        # Pawns
        for col in range(8):
            self._pieces[1][col] = Pawn(Color.WHITE)
            self._pieces[6][col] = Pawn(Color.BLACK)

        for row, color in ((0, Color.WHITE), (7, Color.BLACK)):
            # Rooks
            for col in (0, 7):
                self._pieces[row][col] = Rook(color)
            # Knights
            for col in (1, 6):
                self._pieces[row][col] = Knight(color)
            # Bishops
            for col in (2, 5):
                self._pieces[row][col] = Bishop(color)
            # Queen
            self._pieces[row][3] = Queen(color)
            # King
            self._pieces[row][4] = King(color)

    def get_piece(self, square: Square) -> Piece:
        return self._pieces[square.rank][square.file]

    def set_piece(self, square: Square, piece: Piece):
        self._pieces[square.rank][square.file] = piece

    def remove_piece(self, square: Square):
        self.set_piece(square, None)

    def has_piece(self, square: Square):
        return self.get_piece(square) is not None

    def has_pieces_between(self, src: Square, dst: Square):
        rank_diff = dst.rank - src.rank
        file_diff = dst.file - src.file

        rank_step = rank_diff // max(abs(rank_diff), 1)
        file_step = file_diff // max(abs(file_diff), 1)
        square = Square(file=src.file + file_step, rank=src.rank + rank_step)

        while square != dst:
            if self.has_piece(square):
                return True
            square = Square(file=square.file + file_step, rank=square.rank + rank_step)
        return False
