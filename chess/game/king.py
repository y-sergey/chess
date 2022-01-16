from chess.game.piece import Piece


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, Piece.KING, color)
