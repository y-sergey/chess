from chess.game.piece import Piece


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.QUEEN, color)
