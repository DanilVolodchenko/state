import abc
from queue import Queue, Empty

from interfaces import ICommand
from server import ServerThread
from handlers import ExceptionHandler


class IBehavior(abc.ABC):
    @abc.abstractmethod
    def handle(self, queue: Queue[ICommand]) -> None:
        ...


class NormalBehavior(IBehavior):

    def handle(self, queue: Queue[ICommand]) -> None:
        try:
            cmd = queue.get(timeout=0.3)
        except Empty:
            return

        try:
            cmd.execute()
        except Exception as exc:
            ExceptionHandler.handler(type(exc)).handle(cmd, exc)


class SoftBehavior(IBehavior):

    def handle(self, queue: Queue[ICommand]) -> None:
        try:
            cmd = queue.get(timeout=0.3)
        except Empty:
            thread = ServerThread.get_current_instance()
            thread.stop()
        else:
            try:
                cmd.execute()
            except Exception as exc:
                print(f'({exc.__class__.__name__}) {exc}')


class MoveToBehavior(IBehavior):
    def __init__(self, extra_queue: Queue[ICommand]) -> None:
        self.extra_queue = extra_queue

    def handle(self, queue: Queue[ICommand]) -> None:
        try:
            cmd = queue.get(timeout=0.3)
        except Empty:
            return

        self.extra_queue.put(cmd)
