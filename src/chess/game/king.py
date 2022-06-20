from typing import List

from chess.game.color import Color
from chess.game.constants import File
from chess.game.constants import Rank
from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.piece_table_values import KING_MIDDLE_GAME
from chess.game.square import Square


class King(Piece):
    _START_FILE = File.E
    _MOVE_STEPS = [(-1, -1), (-1, 1), (1, -1), (1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, color):
        Piece.__init__(
            self,
            Piece.KING,
            color,
            material_value=20000,
            piece_table_value=KING_MIDDLE_GAME)
        self._start_rank = Rank.R1 if color == Color.WHITE else Rank.R8

    def can_move(self, src: Square, dst: Square, game_board, pawn_promotion_piece: Piece) -> bool:
        return (self.__can_castle(src, dst, game_board) if self.is_castle_move(src, dst)
                else self.threatens(src, dst, game_board))

    def is_castle_move(self, src: Square, dst: Square) -> bool:
        return (src.rank == self._start_rank and src.file == King._START_FILE
                and dst.rank == src.rank and abs(dst.file - src.file) == 2)

    def get_castle_rook_square(self, dest: Square) -> Square:
        return Square(rank=self._start_rank, file=King.__get_castle_rook_file(dest))

    def get_target_castle_rook_square(self, dest: Square) -> Square:
        return Square(rank=self._start_rank, file=King.__get_target_castle_rook_file(dest))

    def __can_castle(self, src: Square, dst: Square, game_board) -> bool:
        rook_file = King.__get_castle_rook_file(dst)
        rook_square = Square(rank=dst.rank, file=rook_file)
        rook = game_board.get_piece_by_square(rook_square)

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
        return File.H if dst.file > King._START_FILE else File.A

    @staticmethod
    def __get_target_castle_rook_file(dst: Square) -> File:
        return File.F if dst.file > King._START_FILE else File.D

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = abs(dst.rank - src.rank)
        file_diff = abs(dst.file - src.file)
        return (rank_diff == 0 and file_diff == 1
                or file_diff == 0 and rank_diff == 1
                or file_diff == 1 and rank_diff == 1)

    def get_available_moves(self, src: Square, game_board) -> List[Move]:
        for move in super()._get_available_moves_by_steps(src, game_board, King._MOVE_STEPS):
            yield move
        short_castle_square = Square(rank=self._start_rank, file=File.G)
        long_castle_square = Square(rank=self._start_rank, file=File.C)
        for dest in [short_castle_square, long_castle_square]:
            if self.__can_castle(src, dest, game_board):
                yield Move(source=src, dest=dest, piece=self)

    def is_threatened_on_line(self, src: Square, dst: Square, game_board) -> bool:
        rank_diff = dst.rank - src.rank
        file_diff = dst.file - src.file
        same_diagonal = abs(rank_diff) == abs(file_diff)
        same_line = rank_diff == 0 or file_diff == 0
        if not (same_diagonal or same_line):
            return False
        rank_step = rank_diff // max(abs(rank_diff), 1)
        file_step = file_diff // max(abs(file_diff), 1)

        rank = src.rank + rank_step
        file = src.file + file_step
        piece = None
        while File.is_valid(file) and Rank.is_valid(rank):
            piece = game_board.get_piece(file=file, rank=rank)
            if piece:
                break
            else:
                rank += rank_step
                file += file_step
        if not piece:
            return False
        if piece.color() == self.color():
            return False
        if same_diagonal and (piece.name() == Piece.QUEEN or piece.name() == Piece.BISHOP):
            return True
        if same_line and (piece.name() == Piece.QUEEN or piece.name() == Piece.ROOK):
            return True
        return False

