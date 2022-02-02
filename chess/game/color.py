from enum import Enum
from enum import unique


@unique
class Color(Enum):
    WHITE = 1
    BLACK = 2

    @staticmethod
    def opposite(color):
        return Color.WHITE if color == Color.BLACK else Color.BLACK
