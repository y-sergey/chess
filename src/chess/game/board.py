import functools
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
        self._pieces = [
            [None for _ in range(constants.NUM_FILES)] for _ in range(constants.NUM_RANKS)
        ]
        self._king_pos = [None, None]
        self._pieces_by_square = [{}, {}]
        # Pawns
        for file in range(File.A, File.H + 1):
            self.set_piece(Square(rank=Rank.R2, file=file), Pawn(Color.WHITE))
            self.set_piece(Square(rank=Rank.R7, file=file), Pawn(Color.BLACK))

        for rank, color in ((Rank.R1, Color.WHITE), (Rank.R8, Color.BLACK)):
            # Rooks
            for file in [File.A, File.H]:
                self.set_piece(Square(rank=rank, file=file), Rook(color))
            # Knights
            for file in [File.B, File.G]:
                self.set_piece(Square(rank=rank, file=file), Knight(color))
            # Bishops
            for file in [File.C, File.F]:
                self.set_piece(Square(rank=rank, file=file), Bishop(color))
            # Queen
            self.set_piece(Square(rank=rank, file=File.D), Queen(color))
            # King
            self.set_piece(Square(rank=rank, file=File.E), King(color))

    def get_piece(self, square: Square) -> Piece:
        return self._pieces[square.rank][square.file]

    def set_piece(self, square: Square, piece: Piece) -> None:
        self._pieces[square.rank][square.file] = piece
        self._pieces_by_square[Color.WHITE.value].pop(square, None)
        self._pieces_by_square[Color.BLACK.value].pop(square, None)
        if piece:
            self._pieces_by_square[piece.color().value][square] = piece
        if piece and piece.name() == Piece.KING:
            self._king_pos[piece.color().value] = square

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
        return list(self._pieces_by_square[color.value].items())

    def get_king_square(self, color: Color) -> Square:
        return self._king_pos[color.value]

    def get_material_count(self, color: Color) -> int:
        values = [piece.material_value() for square, piece in self.get_pieces_by_color(color)]
        return functools.reduce(lambda a, b: a + b, values, 0)

    def get_material_advantage(self, color: Color) -> int:
        player_material = self.get_material_count(color)
        opponent_material = self.get_material_count(color.opposite())
        return player_material - opponent_material
