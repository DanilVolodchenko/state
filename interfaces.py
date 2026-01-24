import abc


class ICommand(abc.ABC):

    @abc.abstractmethod
    def execute(self) -> None:
        """Выполнение какого-то действия."""


class IHandler(abc.ABC):

    @abc.abstractmethod
    def handle(self, cmd: ICommand, exc: Exception) -> None:
        """Метод для обработки."""

    def __str__(self) -> str:
        return self.__class__.__name__
