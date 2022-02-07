from enum import Enum
from enum import unique


@unique
class Color(Enum):
    WHITE = 1
    BLACK = 2

    def opposite(self):
        return Color.WHITE if self == Color.BLACK else Color.BLACK
