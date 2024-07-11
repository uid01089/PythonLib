from typing import Generic, TypeVar, Callable, Union

from PythonLib.Stream import Stream

T = TypeVar('T')
U = TypeVar('U')


class Optional(Generic[T]):
    def __init__(self, value: Union[T, None]):
        self._value = value

    def is_present(self) -> bool:
        return self._value is not None

    def get(self) -> T:
        if self._value is None:
            raise ValueError("No value present")
        return self._value

    def orElse(self, other: T) -> T:
        return self._value if self._value is not None else other

    def ifPresent(self, consumer: Callable[[T], None]):
        if self._value is not None:
            consumer(self._value)

    def map(self, mapper: Callable[[T], U]) -> 'Optional[U]':
        if self._value is not None:
            return Optional(mapper(self._value))
        return Optional(None)

    def toStream(self) -> Stream[T]:
        """
        Convert this Optional object to a Stream.

        Returns:
            Stream[T]: A Stream containing the value if present, otherwise an empty Stream.
        """
        if self._value is not None:
            return Stream.of(self._value)
        else:
            return Stream([])
