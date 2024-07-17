from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
from types import NoneType
from typing import Callable, Generic, TypeVar, List, Set, Union, Generator, Any, Iterable
import multiprocessing

# Define generic type variables
T = TypeVar('T')
R = TypeVar('R')


class Stream(Generic[T]):
    """
    This class provides a functional-style stream for processing data using various operations such as map, filter, and more.
    """
    MAX_WORKERS = multiprocessing.cpu_count()

    def __init__(self, data: Union[List[T], Set[T]]):
        """
        Initialize a Stream object with the given data.

        Args:
            data (List[T] | Set[T]): The input data for the stream.
        """
        self.data = list(data)

    def map(self, f: Callable[[T], R]) -> Stream[R]:
        """
        Apply a function to each element of the stream.

        Args:
            f (Callable[[T], R]): The function to apply to each element.

        Returns:
            Stream[R]: A new Stream with the modified data.
        """
        self.data = list(map(f, self.data))

        # Remove all None and NoneTypes from collection
        self.filter(lambda value: value is not None and not isinstance(value, NoneType))

        return self

    def mapP(self, f: Callable[[T], R]) -> Stream[R]:
        """
        Parallel version of map using multiprocessing.

        Args:
            f (Callable[[T], R]): The function to apply to each element.

        Returns:
            Stream[R]: A new Stream with the modified data.
        """
        chunkSize = max(min(len(self.data) // Stream.MAX_WORKERS, 2000), 1)

        with ProcessPoolExecutor(max_workers=Stream.MAX_WORKERS) as e:
            res = list(e.map(f, self.data, timeout=None, chunksize=chunkSize))

        self.data = res

        # Remove all None and NoneTypes from collection
        self.filter(lambda value: value is not None and not isinstance(value, NoneType))

        return self

    def filter(self, f: Callable[[T], bool]) -> Stream[T]:
        """
        Filter elements in the stream based on a condition.

        Args:
            f (Callable[[T], bool]): The filter condition function.

        Returns:
            Stream[T]: A new Stream with filtered data.
        """
        self.data = self._filterFct(self.data, f)
        return self

    def flatMap(self, f: Callable[[T], Stream[R]]) -> Stream[R]:
        """
        Apply a function to each element of the stream and flatten the result.

        Args:
            f (Callable[[T], Stream[R]]): The function to apply to each element,
                                           which returns a Stream.

        Returns:
            Stream[R]: A new Stream with the flattened data.
        """
        flattened_data = [item for sublist in map(lambda x: f(x).collectToList(), self.data) for item in sublist]
        return Stream(flattened_data)

    def _filterFct(self, data: List[T], f: Callable[[T], bool]) -> List[T]:
        """
        Filter elements in the stream based on a condition.

        Args:
            data (List[T]): The data to filter.
            f (Callable[[T], bool]): The filter condition function.

        Returns:
            List[T]: A list containing the filtered data.
        """
        return [d for d in data if f(d)]

    def _chunks(self, collection: List[T], n: int) -> Generator[List[T], None, None]:
        """
        Yield n number of striped chunks from a list.

        Args:
            collection (List[T]): The list to split into chunks.
            n (int): The number of chunks to create.

        Returns:
            Generator[List[T], None, None]: A generator of chunked sublists.
        """
        for i in range(0, n):
            yield collection[i::n]

    def filterP(self, f: Callable[[T], bool]) -> Stream[T]:
        """
        Parallel version of filter using multiprocessing.

        Args:
            f (Callable[[T], bool]): The filter condition function.

        Returns:
            Stream[T]: A new Stream with filtered data.
        """
        chunksOfLists = list(self._chunks(self.data, Stream.MAX_WORKERS))
        futureList = []

        with ProcessPoolExecutor(max_workers=Stream.MAX_WORKERS) as e:
            for chunk in chunksOfLists:
                futureList.append(e.submit(self._filterFct, chunk, f))
                # break

            self.data = []

            for fut in as_completed(futureList):
                result = fut.result()
                self.data.extend(result)

        return self

    def foreach(self, f: Callable[[T], Any]) -> None:
        """
        Apply a function to each element of the stream.

        Args:
            f (Callable[[T], Any]): The function to apply to each element.
        """
        list(map(f, self.data))

    def foreachP(self, f: Callable[[T], Any]) -> None:
        """
        Parallel version of foreach using multiprocessing.

        Args:
            f (Callable[[T], Any]): The function to apply to each element.
        """
        with ProcessPoolExecutor(max_workers=Stream.MAX_WORKERS) as e:
            list(e.map(f, self.data))

    def collectToList(self) -> List[T]:
        """
        Collect the stream data into a list.

        Returns:
            List[T]: A list containing the stream data.
        """
        return list(self.data)

    def collectToSet(self) -> Set[T]:
        """
        Collect the stream data into a set.

        Returns:
            Set[T]: A set containing the stream data.
        """
        return set(self.data)

    @staticmethod
    def of(*values: T) -> Stream[T]:
        """
        Create a Stream from the given values.

        Args:
            values (T): The values to include in the Stream.

        Returns:
            Stream[T]: A Stream containing the provided values.
        """
        return Stream(list(values))
