from queue import Queue

from interfaces import ICommand
from server import ServerThread
from state import IState, NormalState, MoveToState, SoftState


class StartServerCommand(ICommand):
    def __init__(self, queue: Queue[ICommand], commands: list[ICommand], state: IState = NormalState()) -> None:
        self._queue = queue
        self._commands = commands
        self._state = state

    def execute(self) -> None:
        for command in self._commands:
            self._queue.put(command)

        thread = ServerThread(self._queue, self._state)
        thread.start()


class HardStopCommand(ICommand):

    def execute(self) -> None:
        thread = ServerThread.get_current_instance()
        thread.stop()


class SoftStopCommand(ICommand):

    def execute(self) -> None:
        thread = ServerThread.get_current_instance()
        thread.state = SoftState()


class MoveToCommand(ICommand):
    def __init__(self, new_queue: Queue[ICommand]) -> None:
        self.new_queue = new_queue

    def execute(self) -> None:
        thread = ServerThread.get_current_instance()
        thread.state = MoveToState(self.new_queue)
