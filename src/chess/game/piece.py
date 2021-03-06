from typing import List
from typing import Tuple

from chess.game.color import Color
from chess.game.constants import File
from chess.game.constants import GamePhase
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

    def __init__(self,
                 name: str,
                 color: Color,
                 material_value: int,
                 piece_table_value: List[List[int]]):
        self._name = name
        self._color = color
        self._num_moves = 0
        self._material_value = material_value
        self._piece_table_value = piece_table_value

    def name(self) -> str:
        return self._name

    def color(self) -> Color:
        return self._color

    def num_moves(self) -> int:
        return self._num_moves

    def increment_moves(self) -> None:
        self._num_moves = self._num_moves + 1

    def decrement_moves(self) -> None:
        self._num_moves = self._num_moves - 1

    def material_value(self):
        return self._material_value

    def position_value(self, square: Square, phase: GamePhase) -> int:
        rank = square.rank if self.color() == Color.WHITE else Rank.mirror(square.rank)
        return self._piece_table_value[rank][square.file]

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

    def get_available_moves(self, src: Square, game_board) -> List[Move]:
        """
        Returns all available moves for this piece given its position and the board.
        This method doesn't take it into account that the king currently can be in check
        or get into check after the move.
        """
        return []

    def _search_available_moves_by_steps(self,
                                         src: Square,
                                         game_board,
                                         rank_and_file_steps: List[Tuple[int, int]]) -> List[Move]:
        for rank_step, file_step in rank_and_file_steps:
            rank = src.rank + rank_step
            file = src.file + file_step
            while File.is_valid(file) and Rank.is_valid(rank):
                target = game_board.get_piece(file, rank)
                if not target or target.color() != self.color():
                    move = Move(source=src, dest=Square(file=file, rank=rank),
                                piece=self, captured=target)
                    yield move
                    rank = rank + rank_step
                    file = file + file_step
                if target is not None:
                    break

    def _get_available_moves_by_steps(self,
                                      src: Square,
                                      game_board,
                                      rank_and_file_steps: List[Tuple[int, int]]) -> List[Move]:
        for rank_step, file_step in rank_and_file_steps:
            file = src.file + file_step
            rank = src.rank + rank_step
            if File.is_valid(file) and Rank.is_valid(rank):
                target = game_board.get_piece(file, rank)
                if not target or target.color() != self.color():
                    move = Move(source=src, dest=Square(file=file, rank=rank),
                                piece=self, captured=target)
                    yield move

    def __str__(self) -> str:
        return f'{self._name} - {self._color.name.lower()}'
