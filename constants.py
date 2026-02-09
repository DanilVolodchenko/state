from typing import TypeAlias, Callable
from queue import Queue

from interfaces import ICommand

Behavior: TypeAlias = Callable[[Queue[ICommand]], None]
