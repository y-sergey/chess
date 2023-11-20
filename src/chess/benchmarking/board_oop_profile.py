import profile

from chess.game.board import Board
from chess.game.color import Color

_board = Board()


def _evaluate() -> int:
    color = Color.WHITE
    scores = [0, 0]
    for i in range(8):
        for j in range(8):
            piece = _board.get_piece(i, j)
            if not piece:
                continue
            idx = piece.color().value
            scores[idx] += piece.material_value()
    return scores[color.value] - scores[color.opposite().value]


def main():
    profile.run('for i in range(10000): _evaluate()', sort='cumtime')


if __name__ == '__main__':
    main()
