from typing import List
from typing import Tuple

from chess.game.constants import File
from chess.game.constants import Rank
from chess.game.move import Move
from chess.game.square import Square


class Piece:
    PAWN = 'P'
    KNIGHT = 'N'
    BISHOP = 'B'
    ROOK = 'R'
    QUEEN = 'Q'
    KING = 'K'

    def __init__(self, name, color):
        self._name = name
        self._color = color

    def name(self):
        return self._name

    def color(self):
        return self._color

    def can_move(self, src: Square, dst: Square, game_board, pawn_promotion_piece=None) -> bool:
        """
        Checks if this piece can move from the 'src' square to the 'dst' square.
        For most pieces the logic will be the same as in 'threatens' function,
        except for pawns which move and capture differently, and can also be promoted.
        """
        return self.threatens(src, dst, game_board)

    def threatens(self, src: Square, dst: Square, game_board) -> bool:
        """
        Checks if this piece threatens a square
        (can capture a piece of the opposite color standing on the 'dst' square).
        """
        return False

    def get_available_moves(self, src: Square, game_board):
        """
        Returns all available moves for this piece given its position and the board.
        This method doesn't take it into account that the king currently can be in check
        or get into check after the move.
        """
        return []

    def _search_available_moves_by_steps(self,
                                         src: Square,
                                         game_board,
                                         rank_and_file_steps: List[Tuple[int, int]]):
        moves = []
        for rank_step, file_step in rank_and_file_steps:
            dest = src.add_file(file_step).add_rank(rank_step)
            while File.is_valid(dest.file) and Rank.is_valid(dest.rank):
                target = game_board.get_piece(dest)
                if target and target.color() == self.color():
                    break
                else:
                    move = Move(source=src, dest=dest, piece=self, captured=target)
                    moves.append(move)
                    dest = dest.add_file(file_step).add_rank(rank_step)
        return moves

    def _get_available_moves_by_steps(self,
                                      src: Square,
                                      game_board,
                                      rank_and_file_steps: List[Tuple[int, int]]):
        moves = []
        for rank_step, file_step in rank_and_file_steps:
            dest = src.add_file(file_step).add_rank(rank_step)
            if File.is_valid(dest.file) and Rank.is_valid(dest.rank):
                target = game_board.get_piece(dest)
                if not target or target.color() != self.color():
                    move = Move(source=src, dest=dest, piece=self, captured=target)
                    moves.append(move)
        return moves

    def __str__(self):
        return f'{self._name} - {self._color.name.lower()}'
