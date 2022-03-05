from typing import List

from chess.game.bishop import Bishop
from chess.game.color import Color
from chess.game.constants import File
from chess.game.constants import Rank
from chess.game.knight import Knight
from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.queen import Queen
from chess.game.rook import Rook
from chess.game.square import Square

_ELIGIBLE_PROMOTION_PIECES = {
    Piece.KNIGHT,
    Piece.BISHOP,
    Piece.ROOK,
    Piece.QUEEN
}


class Pawn(Piece):
    def __init__(self, color: Color):
        Piece.__init__(self, Piece.PAWN, color, material_value=1)
        if color == Color.WHITE:
            self._start_rank = Rank.R2
            self._end_rank = Rank.R8
            self._step = 1
        else:
            self._start_rank = Rank.R7
            self._end_rank = Rank.R1
            self._step = -1

    def end_rank(self) -> int:
        return self._end_rank

    def can_move(self, src: Square, dst: Square, game_board, pawn_promotion_piece: Piece) -> bool:
        if src.file == dst.file:
            # Move one step forward
            if src.rank + self._step == dst.rank and not game_board.has_piece(dst):
                return self._validate_promotion(dst, pawn_promotion_piece)
            # Move 2 steps forward from the initial position
            if (src.rank == self._start_rank
                    and dst.rank == src.rank + 2 * self._step
                    and not game_board.has_piece(src.add_rank(self._step))
                    and not game_board.has_piece(dst)):
                return self._validate_promotion(dst, pawn_promotion_piece)
            return False

        return self.threatens(src, dst, game_board) \
               and self._validate_promotion(dst, pawn_promotion_piece)

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        # A pawn can capture a piece diagonally
        return (dst.rank == src.rank + self._step
                and dst.file in [src.file - 1, src.file + 1]
                and game_board.has_piece(dst))

    def get_available_moves(self, src: Square, game_board) -> List[Move]:
        step_by_one = src.add_rank(self._step)
        can_promote = src.rank == self._end_rank - self._step and not game_board.has_piece(step_by_one)
        promo_squares = []

        if not game_board.has_piece(step_by_one):
            if can_promote:
                promo_squares.append(step_by_one)
            else:
                yield Move(source=src, dest=step_by_one, piece=self)
            if src.rank == self._start_rank:
                step_by_two = step_by_one.add_rank(self._step)
                if not game_board.has_piece(step_by_two):
                    yield Move(source=src, dest=step_by_two, piece=self)

        next_rank = src.rank + self._step
        left_file = src.file + 1
        right_file = src.file - 1
        capture_squares = []
        if Rank.is_valid(next_rank):
            files = filter(File.is_valid, [left_file, right_file])
            capture_squares = map(lambda f: Square(rank=next_rank, file=f), files)
        for square in capture_squares:
            piece = game_board.get_piece(square)
            if piece and piece.color() != self.color():
                if square.rank == self._end_rank:
                    promo_squares.append(square)
                else:
                    yield Move(source=src, dest=square, piece=self, captured=piece)

        for move in self._get_promo_moves(src, promo_squares, game_board):
            yield move

    def _get_promo_moves(self, src: Square, dest_list: List[Square], game_board) -> List[Move]:
        color = self.color()
        for dest in dest_list:
            for promo_piece in [Queen(color), Rook(color), Bishop(color), Knight(color)]:
                yield Move(
                    piece=self,
                    source=src,
                    dest=dest,
                    pawn_promotion_piece=promo_piece,
                    captured=game_board.get_piece(dest))

    def _validate_promotion(self, dst: Square, pawn_promotion_piece: Piece) -> bool:
        if dst.rank != self._end_rank and pawn_promotion_piece:
            return False
        if dst.rank == self._end_rank and not pawn_promotion_piece:
            return False
        if dst.rank == self._end_rank \
                and not pawn_promotion_piece.name() in _ELIGIBLE_PROMOTION_PIECES:
            return False
        return True
