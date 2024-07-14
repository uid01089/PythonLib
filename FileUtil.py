import os
import hashlib
import re
import shutil
import logging
from re import Pattern
from typing import Callable, List, Tuple, Optional
from pathlib import Path
from PythonLib.Stream import Stream

# Initialize a logger for the FileOperations class
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
        return bool(pattern.match(pathStr))

    @staticmethod
    def getPaths(directory: Path, regex: str) -> List[Path]:
        """
        Get a list of paths within a directory that match a regular expression pattern.

        Args:
            directory (Path): The directory to search for files in.
            regex (str): The regular expression pattern to match against.

        Returns:
            List[Path]: A list of Path objects representing matching files.
        """
        pattern = re.compile(regex, re.IGNORECASE | re.DOTALL)
        allFiles: List[Path] = []

        for file in directory.rglob('*'):
            if file.is_file():
                allFiles.append(file)

        allFilesFiltered = Stream(allFiles) \
            .filter(lambda path: FileOperations._getPathsFilter(path, pattern)) \
            .map(Path) \
            .collectToSet()

        return list(allFilesFiltered)

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
        BUF_SIZE = 65536  # Read in chunks of 64KB
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
    def getFilesAndDirectories(path: Path) -> Tuple[List[Path], List[Path]]:
        """
        Get all files and directories within a given path.

        Args:
            path (Path): The path to search.

        Returns:
            Tuple[List[Path], List[Path]]: A tuple containing a list of files and a list of directories.
        """
        files: List[Path] = []
        directories: List[Path] = []

        for item in path.iterdir():
            if item.is_file():
                files.append(item)
            else:
                directories.append(item)

        return (files, directories)

    @staticmethod
    def treeWalker(startPath: Path, fileVisitor: Optional[Callable[[Path], None]] = None,
                   dirVisitor: Optional[Callable[[Path], None]] = None,
                   dirLeaver: Optional[Callable[[Path], None]] = None) -> None:
        """
        Recursively walk through a directory tree, applying visitors to files and directories.

        Args:
            startPath (Path): The starting directory.
            fileVisitor (Optional[Callable[[Path], None]]): Function to call on each file.
            dirVisitor (Optional[Callable[[Path], None]]): Function to call before entering each directory.
            dirLeaver (Optional[Callable[[Path], None]]): Function to call after leaving each directory.
        """

        if dirVisitor:
            dirVisitor(startPath)

        files, directories = FileOperations.getFilesAndDirectories(startPath)

        for directory in directories:
            FileOperations.treeWalker(directory, fileVisitor, dirVisitor, dirLeaver)

        for file in files:
            if fileVisitor:
                fileVisitor(file)

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
        """
        Check if a directory is a child of another directory.

        Args:
            parentDirectory (Path): The parent directory.
            childDirectory (Path): The suspected child directory.

        Returns:
            bool: True if the child is a subdirectory of the parent, False otherwise.
        """
        return childDirectory.as_posix().startswith(parentDirectory.as_posix())

    @staticmethod
    def as_cygwin(path: Path) -> Path:
        """
        Convert a Windows path to a Cygwin-compatible path.

        Args:
            path (Path): The input Windows path.

        Returns:
            Path: The converted Cygwin-compatible path.
        """
        cygwinPath = path.as_posix()
        if path.drive:
            cygwinPath = cygwinPath.replace(f"{path.drive}", f"/cygdrive/{path.drive[0].lower()}")
        return Path(cygwinPath)

    @staticmethod
    def getAllFilesOfAnDirectory(directory_path: Path) -> List[Path]:
        """
        Get all files within a given directory.

        Args:
            directory_path (Path): The directory to search.

        Returns:
            List[Path]: A list of Path objects representing the files.
        """
        return [path for path in directory_path.iterdir() if path.is_file()]

    @staticmethod
    def getAllDirsOfAnDirectory(directory_path: Path) -> List[Path]:
        """
        Get all directories within a given directory.

        Args:
            directory_path (Path): The directory to search.

        Returns:
            List[Path]: A list of Path objects representing the directories.
        """
        return [path for path in directory_path.iterdir() if path.is_dir()]
