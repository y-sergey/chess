import sys
from typing import List

from chess.game.color import Color
from chess.game.constants import File
from chess.game.constants import Rank
from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.square import Square


class King(Piece):
    _START_FILE = File.FILE_E.value

    def __init__(self, color):
        Piece.__init__(self, Piece.KING, color, material_value=sys.maxsize)
        self._start_rank = Rank.RANK_1.value if color == Color.WHITE else Rank.RANK_8.value

    def can_move(self, src: Square, dst: Square, game_board, pawn_promotion_piece: Piece) -> bool:
        return (self.__can_castle(src, dst, game_board) if self.is_castle_move(src, dst)
                else self.threatens(src, dst, game_board))

    def is_castle_move(self, src: Square, dst: Square) -> bool:
        return (src.rank == self._start_rank and src.file == King._START_FILE
                and dst.rank == src.rank and abs(dst.file - src.file) == 2)

    def get_castle_rook_square(self, dest: Square) -> Square:
        return Square(rank=self._start_rank, file=King.__get_castle_rook_file(dest).value)

    def get_target_castle_rook_square(self, dest: Square) -> Square:
        return Square(rank=self._start_rank, file=King.__get_target_castle_rook_file(dest).value)

    def __can_castle(self, src: Square, dst: Square, game_board) -> bool:
        rook_file = King.__get_castle_rook_file(dst)
        rook_square = Square(rank=dst.rank, file=rook_file.value)
        rook = game_board.get_piece(rook_square)

        # The king must be on the start square
        if src.file != King._START_FILE or src.rank != self._start_rank:
            return False
        # Check if there is a rook
        if not rook or rook.name() != Piece.ROOK or rook.color() != self.color():
            return False
        # Check there are no pieces between the rook and the king
        if game_board.has_pieces_between(src, rook_square):
            return False
        # Check that both the king and the king haven't moved yet
        if rook.num_moves() > 0 or self.num_moves() > 0:
            return False
        # Check that the king and the squares between the king and the rook
        # aren't threatened (the king can't be in check and can't go through check).
        file_step = (dst.file - src.file) // abs(dst.file - src.file)
        for piece_square, piece in game_board.get_pieces_by_color(self.color().opposite()):
            # The king moves by 2 squares while castling
            for file in range(src.file, src.file + 3 * file_step, file_step):
                square = Square(rank=src.rank, file=file)
                if piece.threatens(piece_square, square, game_board):
                    return False
        return True

    @staticmethod
    def __get_castle_rook_file(dst: Square) -> File:
        return File.FILE_H if dst.file > King._START_FILE else File.FILE_A

    @staticmethod
    def __get_target_castle_rook_file(dst: Square) -> File:
        return File.FILE_F if dst.file > King._START_FILE else File.FILE_D

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = abs(dst.rank - src.rank)
        file_diff = abs(dst.file - src.file)
        return (rank_diff == 0 and file_diff == 1
                or file_diff == 0 and rank_diff == 1
                or file_diff == 1 and rank_diff == 1)

    def get_available_moves(self, src: Square, game_board) -> List[Move]:
        rank_and_file_steps = [(-1, -1), (-1, 1), (1, -1), (1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)]
        moves = super()._get_available_moves_by_steps(src, game_board, rank_and_file_steps)
        short_castle_square = Square(rank=self._start_rank, file=File.FILE_G.value)
        long_castle_square = Square(rank=self._start_rank, file=File.FILE_C.value)
        for dest in [short_castle_square, long_castle_square]:
            if self.__can_castle(src, dest, game_board):
                moves.append(Move(source=src, dest=dest, piece=self))
        return moves
