import os
import hashlib
import re
import shutil
import logging
from re import Pattern
from typing import Callable
from pathlib import Path
from PythonLib.Stream import Stream

logger = logging.getLogger('FileOperations')

# This class provides various file and directory operations.


class FileOperations:
    @staticmethod
    def _getPathsFilter(path: Path, pattern: Pattern) -> bool:
        """
        Determine if a given path matches a regular expression pattern.

        Args:
            path (Path): The path to be checked.
            pattern (Pattern): The regular expression pattern to match against.

        Returns:
            bool: True if the path matches the pattern, False otherwise.
        """
        pathStr = path.as_posix()
        return pattern.match(pathStr)

    @staticmethod
    def getPaths(directory: Path, regex: str) -> list[Path]:
        """
        Get a list of paths within a directory that match a regular expression pattern.

        Args:
            directory (Path): The directory to search for files in.
            regex (str): The regular expression pattern to match against.

        Returns:
            list[Path]: A list of Path objects representing matching files.
        """
        pattern = re.compile(regex, re.IGNORECASE | re.DOTALL)

        allFiles = []
        for file in directory.rglob('*'):
            if file.is_file():
                allFiles.append(file)

        allFilesFiltered = Stream(allFiles) \
            .filter(lambda path: FileOperations._getPathsFilter(path, pattern)) \
            .map(Path) \
            .collectToSet()
        return allFilesFiltered

    @staticmethod
    def getSize(path: Path) -> int:
        """
        Get the size of a file.

        Args:
            path (Path): The path to the file.

        Returns:
            int: The size of the file in bytes.
        """
        return path.stat().st_size

    @staticmethod
    def getHash(path: Path) -> str:
        """
        Get the SHA3-256 hash of a file.

        Args:
            path (Path): The path to the file.

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
    def getCwd() -> Path:
        """
        Get the current working directory.

        Returns:
            Path: The current working directory as a Path object.
        """
        return Path(os.getcwd())

    @staticmethod
    def getFilesAndDirectories(path: Path) -> tuple[list[Path], list[Path]]:
        files = []
        directories = []
        for path in path.iterdir():
            if path.is_file():
                files.append(path)
            else:
                directories.append(path)
        return (files, directories)

    @staticmethod
    def treeWalker(startPath: Path, fileVisitor: Callable[[Path], None],
                   dirVisitor: Callable[[Path], None], dirLeaver: Callable[[Path], None]) -> None:

        # Call DirVisitor at first
        if dirVisitor:
            dirVisitor(startPath)

        (files, directories) = FileOperations.getFilesAndDirectories(startPath)

        for path in startPath.iterdir():
            if path.is_file():
                files.append(path)
            else:
                directories.append(path)

       # Dive into the tree
        for directory in directories:
            FileOperations.treeWalker(directory, fileVisitor, dirVisitor, dirLeaver)

        # Call all file visitors
        for file in files:
            if fileVisitor:
                fileVisitor(file)

        # Call dirLeaver
        if dirLeaver:
            dirLeaver(startPath)

    @staticmethod
    def copyFile(source: Path, target: Path) -> None:
        """
        Copy a file from the source path to the target path.

        Args:
            source (Path): The source file path.
            target (Path): The target file path.
        """
        shutil.copy(source, target)

    @staticmethod
    def copyDir(sourceDir: Path, targetDir: Path) -> None:
        """
        Copy a directory and its contents from the source path to the target path.

        Args:
            sourceDir (Path): The source directory path.
            targetDir (Path): The target directory path.
        """
        shutil.copytree(sourceDir, targetDir)

    @staticmethod
    def delTree(directory: Path) -> None:
        """
        Recursively delete a directory and its contents.

        Args:
            directory (Path): The directory to be deleted.
        """
        shutil.rmtree(directory)

    @staticmethod
    def isChild(parentDirectory: Path, childDirectory: Path) -> bool:
        """_summary_

        Args:
            parentDirectory (Path): parent directory
            childDirectory (Path): child directory

        Returns:
            bool: returns if child is really a child of parent
        """

        return childDirectory.as_posix().startswith(parentDirectory.as_posix())

    @staticmethod
    def as_cygwin(path: Path) -> Path:
        cygwinPath = path.as_posix()
        if path.drive:
            cygwinPath = cygwinPath.replace(f"{path.drive}", f"/cygdrive/{path.drive[0].lower()}")
        return Path(cygwinPath)

    @staticmethod
    def getAllFilesOfAnDirectory(directory_path: Path):
        return [path for path in directory_path.iterdir() if path.is_file()]

    @staticmethod
    def getAllDirsOfAnDirectory(directory_path: Path):
        return [path for path in directory_path.iterdir() if path.is_dir()]
