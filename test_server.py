import threading
from queue import Queue
from threading import current_thread

from interfaces import ICommand

from commands import StartServerCommand, HardStopCommand, SoftStopCommand, MoveToCommand
from server import ServerThread


class CommandMock(ICommand):
    def __init__(self):
        self.count_called = 0

    def execute(self) -> None:
        self.count_called += 1


def get_server_thread() -> ServerThread:
    for thread in threading.enumerate():
        if isinstance(thread, ServerThread):
            return thread
    else:
        raise Exception('ServerThread not found')


def stop_all_server_threads() -> None:
    for thread in threading.enumerate():
        if isinstance(thread, ServerThread):
            thread.stop()


def test_server_thread_start() -> None:
    """Тестирование запуска потока."""

    queue = Queue()
    cmd = CommandMock()
    StartServerCommand(queue, [cmd]).execute()

    server_thread: ServerThread = get_server_thread()
    server_thread.stop()
    server_thread.join(timeout=0.5)

    assert isinstance(server_thread, ServerThread), 'Полученный поток должен быть типа ServerThread'


def test_event_synchronization() -> None:
    """Тестирование событий синхронизации."""

    queue = Queue()
    cmd = CommandMock()
    StartServerCommand(queue, [cmd]).execute()

    server_thread: ServerThread = get_server_thread()

    server_thread.stop()
    server_thread.join(timeout=0.5)

    assert server_thread.started_event.is_set() == False, 'Событие должно быть равно False'


def test_server_with_command() -> None:
    """Тестирование запуска потока с тестовыми командами."""

    queue = Queue()
    cmd = CommandMock()
    StartServerCommand(queue, [cmd, cmd]).execute()

    server_thread: ServerThread = get_server_thread()
    server_thread.stop()
    server_thread.join(timeout=0.5)

    result = cmd.count_called
    expected_result = 2

    assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'


def test_server_with_hard_stop_command() -> None:
    """Тестирование запуска потока с командой HardStopCommand."""

    queue = Queue()
    cmd = CommandMock()
    StartServerCommand(queue, [cmd, cmd, HardStopCommand(), cmd]).execute()

    result = cmd.count_called
    expected_result = 2

    assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'


def test_server_with_soft_stop_command() -> None:
    """Тестирование запуска потока с командой SoftStopCommand."""

    queue = Queue()
    cmd = CommandMock()
    StartServerCommand(queue, [cmd, cmd, SoftStopCommand(), cmd]).execute()

    result = cmd.count_called
    expected_result = 3

    assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'


def test_server_with_move_to_command() -> None:
    """Тестирование запуска потока с командой MoveToCommand."""

    queue = Queue()
    new_queue = Queue()
    cmd = CommandMock()
    StartServerCommand(queue, [cmd, cmd, MoveToCommand(new_queue), cmd]).execute()

    stop_all_server_threads()

    assert queue.empty() == True, 'Очередь не должна быть пуста'
