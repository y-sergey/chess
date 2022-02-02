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

    def can_move(self, src: Square, dst: Square, game_board) -> bool:
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

    def __str__(self):
        return f'{self._name} - {self._color.name.lower()}'
