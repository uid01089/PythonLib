import glob as glob
import pathlib as pathlib
import re
from re import Pattern
from ks.Stream import Stream
import os
import hashlib



def _getPathsFilter (path: pathlib.PurePath, pattern: Pattern) -> bool:
   pathStr = path.__str__()
   return pattern.match(pathStr)


def getPaths(dir: str, regEx: str) -> list: #[pathlib.Path]:

   allFiles = []
   pattern = re.compile(regEx, re.IGNORECASE | re.DOTALL)
   
   for path, subdirs, files in os.walk(dir):   
    for name in files:
        allFiles.append(pathlib.PurePath(path, name))

   allFilesFiltered = Stream(allFiles) \
      .filter(lambda path: _getPathsFilter(path, pattern)) \
      .map(pathlib.Path) \
      .collectToSet()
   return allFilesFiltered

def getSize(path : pathlib.PurePath) -> int:
    return path.stat().st_size

def getHash(path: pathlib.PurePath) -> str:
   BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
   m = hashlib.sha3_256()
   with open(path, 'rb') as f:
      while True:
         data = f.read(BUF_SIZE)
         if not data:
               break
         m.update(data)

   return m.hexdigest()

def getCwd() -> pathlib.Path:
   return pathlib.Path(os.getcwd())


