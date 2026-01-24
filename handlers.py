from typing import Type

from interfaces import ICommand, IHandler


class LogHandler(IHandler):

    def handle(self, cmd: ICommand, exc: Exception) -> None:
        print(f'Возникла ошибка ({exc.__class__.__name__}) у команды {cmd.__class__.__name__}: {exc}')


class ExceptionHandler:
    state: dict[Type[Exception], Type[IHandler]] = {}

    @classmethod
    def handler(cls, exc: Type[Exception], *, default_handler: Type[IHandler] = LogHandler) -> IHandler:
        """Возвращает обработчика в зависимости от типа исключения."""

        try:
            return cls.state[exc]()
        except KeyError:
            return default_handler()

    @classmethod
    def register(cls, exc: Type[Exception], handler: Type[IHandler]) -> None:
        cls.state[exc] = handler
