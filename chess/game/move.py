from dataclasses import dataclass

from chess.game.square import Square


@dataclass
class Move:
    source: Square
    dest: Square
    piece: 'Piece'
    captured: 'Piece'
