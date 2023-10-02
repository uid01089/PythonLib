from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing


class Stream:
    """
    This class provides a functional-style stream for processing data using various operations such as map, filter, and more.
    """
    MAX_WORKERS = multiprocessing.cpu_count()

    def __init__(self, data: list | set):
        """
        Initialize a Stream object with the given data.

        Args:
            data (list | set): The input data for the stream.
        """
        self.data = list(data)

    def map(self, f: callable) -> Stream:
        """
        Apply a function to each element of the stream.

        Args:
            f (callable): The function to apply to each element.

        Returns:
            Stream: A new Stream with the modified data.
        """
        self.data = list(map(f, self.data))
        return self

    def mapP(self, f: callable) -> Stream:
        """
        Parallel version of map using multiprocessing.

        Args:
            f (callable): The function to apply to each element.

        Returns:
            Stream: A new Stream with the modified data.
        """
        chunkSize = max(min(len(self.data) // Stream.MAX_WORKERS, 2000), 1)

        with ProcessPoolExecutor(max_workers=Stream.MAX_WORKERS) as e:
            res = list(e.map(f, self.data, timeout=None, chunksize=chunkSize))

        self.data = res
        return self

    def filter(self, f: callable) -> Stream:
        """
        Filter elements in the stream based on a condition.

        Args:
            f (callable): The filter condition function.

        Returns:
            Stream: A new Stream with filtered data.
        """
        self.data = self._filterFct(self.data, f)
        return self

    def _filterFct(self, data: list, f: callable) -> list:
        """
        Filter elements in the stream based on a condition.

        Args:
            data (list): The data to filter.
            f (callable): The filter condition function.

        Returns:
            list: A list containing the filtered data.
        """
        filteredList = [d for d in data if f(d)]
        return filteredList

    def _chunks(self, collection: list, n: int) -> list:
        """
        Yield n number of striped chunks from a list.

        Args:
            collection (list): The list to split into chunks.
            n (int): The number of chunks to create.

        Returns:
            list: A list of chunked sublists.
        """
        for i in range(0, n):
            yield collection[i::n]

    def filterP(self, f: callable) -> Stream:
        """
        Parallel version of filter using multiprocessing.

        Args:
            f (callable): The filter condition function.

        Returns:
            Stream: A new Stream with filtered data.
        """
        chunksOfLists = list(self._chunks(self.data, Stream.MAX_WORKERS))
        futureList = []

        with ProcessPoolExecutor(max_workers=Stream.MAX_WORKERS) as e:
            for chunk in chunksOfLists:
                futureList.append(e.submit(self._filterFct, chunk, f))
                break

            self.data = []

            for fut in as_completed(futureList):
                result = fut.result()
                self.data.extend(result)

        return self

    def foreach(self, f: callable) -> None:
        """
        Apply a function to each element of the stream.

        Args:
            f (callable): The function to apply to each element.
        """
        list(map(f, self.data))

    def foreachP(self, f: callable) -> None:
        """
        Parallel version of foreach using multiprocessing.

        Args:
            f (callable): The function to apply to each element.
        """
        with ProcessPoolExecutor(max_workers=Stream.MAX_WORKERS) as e:
            res = list(e.map(f, self.data))

    def collectToList(self) -> list:
        """
        Collect the stream data into a list.

        Returns:
            list: A list containing the stream data.
        """
        return list(self.data)

    def collectToSet(self) -> set:
        """
        Collect the stream data into a set.

        Returns:
            set: A set containing the stream data.
        """
        return set(self.data)
