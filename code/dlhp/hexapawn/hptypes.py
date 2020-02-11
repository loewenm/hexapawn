import enum
from collections import namedtuple

__all__ = [
    'Player',
    'Point',
]


class Player(enum.Enum):
    x = 1 #white
    o = 2 #black

    @property
    def other(self):
        return Player.x if self == Player.o else Player.o


class Point(namedtuple('Point', 'row col')):
    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self
