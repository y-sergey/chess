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

    def can_move(self, src: Square, dst: Square, board) -> bool:
        return
