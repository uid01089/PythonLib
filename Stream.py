# https://stackoverflow.com/questions/68631015/python-equivalent-of-java-streams-piping

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import multiprocessing

class Stream:

    MAX_WORKERS = multiprocessing.cpu_count()

    def __init__(self, data: list | set):
        self.data = list(data)

    # map(lambda x: x * 2)
    def map(self, f) -> Stream:
        self.data = list(map(f, self.data))
        return self

    def mapP(self, f) -> Stream:
        chunkSize = max(min(len(self.data) // Stream.MAX_WORKERS, 2000), 1)

        with ProcessPoolExecutor(max_workers=Stream.MAX_WORKERS) as e:
            res = list(e.map(f, self.data, timeout=None, chunksize=chunkSize))
        
        self.data =res
        return self

    # filter(lambda x: x > 4)
    def filter(self, f) -> Stream:
        self.data = self._filterFct(self.data, f)
        return self

    def _filterFct(self, data, f) -> list:
        filteredList =   [d for d in data if f(d)]
        return filteredList
    
    def _chunks(self, collection: list, n: int) -> list:
        """Yield n number of striped chunks from l."""
        #https://stackoverflow.com/questions/24483182/python-split-list-into-n-chunks
        for i in range(0, n):
            yield collection[i::n]        

    def filterP(self, f) -> Stream:
        
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

    def foreach(self, f) -> None:
        list(map(f, self.data))

    def foreachP(self, f) -> None:
        with ProcessPoolExecutor(max_workers=Stream.MAX_WORKERS) as e:
            res = list(e.map(f, self.data))

    def collectToList(self) -> list:
        return list(self.data)

    def collectToSet(self) -> set:
        return set(self.data)
