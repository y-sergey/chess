from typing import List

import chess.game.constants as constants
from chess.game.bishop import Bishop
from chess.game.color import Color
from chess.game.constants import File
from chess.game.constants import Rank
from chess.game.king import King
from chess.game.knight import Knight
from chess.game.pawn import Pawn
from chess.game.piece import Piece
from chess.game.queen import Queen
from chess.game.rook import Rook
from chess.game.square import Square


class Board:

    def __init__(self):
        # Outer lists represent ranks (rows). Inner lists represent files (columns).
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

        self._king_pos = {
            Color.WHITE: Square(file=File.FILE_E.value, rank=Rank.RANK_1.value),
            Color.BLACK: Square(file=File.FILE_E.value, rank=Rank.RANK_8.value)
        }

    def get_piece(self, square: Square) -> Piece:
        return self._pieces[square.rank][square.file]

    def set_piece(self, square: Square, piece: Piece) -> None:
        self._pieces[square.rank][square.file] = piece
        if piece and piece.name() == Piece.KING:
            self._king_pos[piece.color()] = square

    def remove_piece(self, square: Square) -> None:
        self.set_piece(square, None)

    def has_piece(self, square: Square) -> bool:
        return self.get_piece(square) is not None

    def has_pieces_between(self, src: Square, dst: Square) -> bool:
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

    def get_pieces_by_color(self, color: Color) -> List[Piece]:
        result = []
        for rank in range(Rank.RANK_1.value, constants.NUM_RANKS):
            for file in range(File.FILE_A.value, constants.NUM_FILES):
                square = Square(file=file, rank=rank)
                piece = self.get_piece(square)
                if piece and piece.color() == color:
                    result.append((piece, square))
        return result

    def get_king_square(self, color: Color) -> Square:
        return self._king_pos[color]
