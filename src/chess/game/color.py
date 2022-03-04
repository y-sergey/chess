from __future__ import annotations

from enum import Enum
from enum import unique


@unique
class Color(Enum):
    WHITE = 0
    BLACK = 1

    def opposite(self) -> Color:
        return Color.WHITE if self == Color.BLACK else Color.BLACK
