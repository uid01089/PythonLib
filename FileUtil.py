import os
import hashlib
import pathlib
import re
import shutil
from re import Pattern
from typing import Callable
from PythonLib.Stream import Stream


def _getPathsFilter(path: pathlib.PurePath, pattern: Pattern) -> bool:
    pathStr = path.__str__()
    return pattern.match(pathStr)


def getPaths(dir: str, regEx: str) -> list:  # [pathlib.Path]:

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


def getSize(path: pathlib.PurePath) -> int:
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


def treeWalker(startPath: pathlib.PurePath, fileVisitor: Callable[[pathlib.PurePath], None],
               dirVisitor: Callable[[pathlib.PurePath], None], dirLeaver: Callable[[pathlib.PurePath], None]) -> None:

    # Call DirVisitor at first
    if dirVisitor:
        dirVisitor(startPath)

    files = []
    directories = []

    for dirElement in os.listdir(startPath):
        path = pathlib.Path(startPath, dirElement)
        if path.is_file():
            files.append(path)
        else:
            directories.append(path)

   # dive into tree
    for directory in directories:
        treeWalker(directory, fileVisitor, dirVisitor, dirLeaver)

    # Call all file visitors
    for file in files:
        fileVisitor(file)

    # Call dirLeaver
    if dirLeaver:
        dirLeaver(startPath)


def copyFile(source: pathlib.PurePath, target: pathlib.PurePath) -> None:
    shutil.copy(source, target)


def copyDir(sourceDir: pathlib.PurePath, targetDir: pathlib.PurePath) -> None:
    shutil.copytree(sourceDir, targetDir)


def delTree(directory: pathlib.PurePath) -> None:
    shutil.rmtree(directory)
