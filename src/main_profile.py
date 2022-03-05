import profile

from chess.bot.minimax_bot import MiniMaxBot
from chess.game.color import Color
from chess.game.constants import File
from chess.game.constants import Rank
from chess.game.game import Game
from chess.game.square import Square

_game = Game()
_bot = MiniMaxBot(Color.BLACK, _game)


def main():
    _game.validate_and_move(
        Square(file=File.E, rank=Rank.RANK_2),
        Square(file=File.E, rank=Rank.RANK_4))
    profile.run('_bot.move()', sort='tottime')


if __name__ == '__main__':
    main()
