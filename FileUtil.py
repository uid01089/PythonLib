import os
import hashlib
import pathlib
import re
import shutil
from re import Pattern
from typing import Callable
from PythonLib.Stream import Stream


# This class provides various file and directory operations.
class FileOperations:
    @staticmethod
    def _getPathsFilter(path: pathlib.PurePath, pattern: Pattern) -> bool:
        """
        Determine if a given path matches a regular expression pattern.

        Args:
            path (pathlib.PurePath): The path to be checked.
            pattern (Pattern): The regular expression pattern to match against.

        Returns:
            bool: True if the path matches the pattern, False otherwise.
        """
        pathStr = path.__str__()
        return pattern.match(pathStr)

    @staticmethod
    def getPaths(dir: str, regex: str) -> list[pathlib.Path]:
        """
        Get a list of paths within a directory that match a regular expression pattern.

        Args:
            dir (str): The directory to search for files in.
            regex (str): The regular expression pattern to match against.

        Returns:
            list[pathlib.Path]: A list of pathlib.Path objects representing matching files.
        """
        allFiles = []
        pattern = re.compile(regex, re.IGNORECASE | re.DOTALL)

        for path, subdirs, files in os.walk(dir):
            for name in files:
                allFiles.append(pathlib.PurePath(path, name))

        allFilesFiltered = Stream(allFiles) \
            .filter(lambda path: FileOperations._getPathsFilter(path, pattern)) \
            .map(pathlib.Path) \
            .collectToSet()
        return allFilesFiltered

    @staticmethod
    def getSize(path: pathlib.PurePath) -> int:
        """
        Get the size of a file.

        Args:
            path (pathlib.PurePath): The path to the file.

        Returns:
            int: The size of the file in bytes.
        """
        return path.stat().st_size

    @staticmethod
    def getHash(path: pathlib.PurePath) -> str:
        """
        Get the SHA3-256 hash of a file.

        Args:
            path (pathlib.PurePath): The path to the file.

        Returns:
            str: The hexadecimal representation of the file's hash.
        """
        BUF_SIZE = 65536  # Let's read stuff in 64KB chunks!
        m = hashlib.sha3_256()
        with open(path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                m.update(data)

        return m.hexdigest()

    @staticmethod
    def getCwd() -> pathlib.Path:
        """
        Get the current working directory.

        Returns:
            pathlib.Path: The current working directory as a pathlib.Path object.
        """
        return pathlib.Path(os.getcwd())

    @staticmethod
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

       # Dive into the tree
        for directory in directories:
            FileOperations.treeWalker(directory, fileVisitor, dirVisitor, dirLeaver)

        # Call all file visitors
        for file in files:
            fileVisitor(file)

        # Call dirLeaver
        if dirLeaver:
            dirLeaver(startPath)

    @staticmethod
    def copyFile(source: pathlib.PurePath, target: pathlib.PurePath) -> None:
        """
        Copy a file from the source path to the target path.

        Args:
            source (pathlib.PurePath): The source file path.
            target (pathlib.PurePath): The target file path.
        """
        shutil.copy(source, target)

    @staticmethod
    def copyDir(sourceDir: pathlib.PurePath, targetDir: pathlib.PurePath) -> None:
        """
        Copy a directory and its contents from the source path to the target path.

        Args:
            sourceDir (pathlib.PurePath): The source directory path.
            targetDir (pathlib.PurePath): The target directory path.
        """
        shutil.copytree(sourceDir, targetDir)

    @staticmethod
    def delTree(directory: pathlib.PurePath) -> None:
        """
        Recursively delete a directory and its contents.

        Args:
            directory (pathlib.PurePath): The directory to be deleted.
        """
        shutil.rmtree(directory)
