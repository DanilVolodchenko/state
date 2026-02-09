from queue import Queue
import threading

from interfaces import ICommand
from constants import Behavior
from state import IState


class ServerThread(threading.Thread):
    __thread_instances = {}

    def __init__(self, queue: Queue[ICommand], state: IState, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.state = state
        self.started_event = threading.Event()

    @property
    def behavior(self) -> Behavior:
        return self._behavior

    @behavior.setter
    def behavior(self, new_behavior: Behavior) -> None:
        self._behavior = new_behavior

    def run(self) -> None:
        cls = self.__class__
        cls.__thread_instances[self.ident] = self
        self.started_event.set()

        while self.started_event.is_set():
            behavior = self.state.get_behavior()
            behavior(self.queue)

    def stop(self) -> None:
        self.started_event.clear()

    @classmethod
    def get_current_instance(cls) -> 'ServerThread':
        return cls.__thread_instances[threading.get_ident()]
