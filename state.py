import abc
from collections.abc import Callable
from queue import Queue

from commands import ICommand


class IState(abc.ABC):
    @abc.abstractmethod
    def get_behavior(self):
        """Возвращает поведение."""


class NormalState(IState):
    def get_behavior(self):
        from behaviors import NormalBehavior

        return NormalBehavior().handle


class SoftState(IState):
    def get_behavior(self):
        from behaviors import SoftBehavior

        return SoftBehavior().handle

class MoveToState(IState):
    def __init__(self, extra_queue: Queue[ICommand]):
        self.extra_queue = extra_queue

    def get_behavior(self):
        from behaviors import MoveToBehavior

        return MoveToBehavior(extra_queue=self.extra_queue).handle
