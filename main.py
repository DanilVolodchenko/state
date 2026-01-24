import queue

from commands import StartServerCommand, HardStopCommand, MoveToCommand
from server import ServerThread
from interfaces import ICommand
from state import NormalState, MoveToState


class CommandMock(ICommand):
    def __init__(self):
        self.count_called = 0

    def execute(self) -> None:
        print('hello')
        self.count_called += 1

import threading

def get_server_thread() -> ServerThread:
    for thread in threading.enumerate():
        if isinstance(thread, ServerThread):
            return thread
    else:
        raise Exception('ServerThread not found')

if __name__ == '__main__':
    main_queue = queue.Queue()
    new_queue = queue.Queue()
    StartServerCommand(
        queue=main_queue, commands= [CommandMock(), CommandMock(), MoveToCommand(new_queue), CommandMock()]
    ).execute()

    import time
    time.sleep(0.1)
    assert main_queue.empty() == True
    th = get_server_thread()
    th.stop()
    assert new_queue.empty() == False
