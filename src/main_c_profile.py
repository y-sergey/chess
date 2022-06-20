from chess.bot.minimax_bot import MiniMaxBot
from chess.game.color import Color
from chess.game.constants import File
from chess.game.constants import Rank
from chess.game.game import Game
from chess.game.square import Square


def main():
    game = Game()
    bot = MiniMaxBot(Color.BLACK, game)

    game.validate_and_move(
        Square(file=File.E, rank=Rank.R2),
        Square(file=File.E, rank=Rank.R4))
    bot.move()


if __name__ == '__main__':
    main()
