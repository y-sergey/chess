from dataclasses import dataclass
from dataclasses import field

from chess.game.square import Square


@dataclass
class Move:
    source: Square
    dest: Square
    piece: 'Piece'
    captured: 'Piece' = field(default=None)
    pawn_promotion_piece: 'Piece' = field(default=None)

    def __str__(self):
        return f'{self.piece.name()}{self.source}-{self.dest}'

    def __repr__(self):
        return self.__str__()
