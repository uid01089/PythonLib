from __future__ import annotations
from pathlib import PurePath
import subprocess


# This class provides a simplified interface for interacting with Git repositories using subprocess.
class Git:
    def __init__(self, workingDir: PurePath) -> None:
        """
        Initialize a Git object for a specific working directory.

        Args:
            workingDir (PurePath): The path to the Git working directory.
        """
        self.workingDir = workingDir

    def init(self) -> Git:
        """
        Initialize a Git repository in the working directory.

        Returns:
            Git: The current Git object.
        """
        subprocess.call(["git.exe", "init"], shell=True, cwd=self.workingDir)
        return self

    def initBare(self) -> Git:
        """
        Initialize a bare Git repository in the working directory.

        Returns:
            Git: The current Git object.
        """
        subprocess.call(["git.exe", "init", "--bare"], shell=True, cwd=self.workingDir)
        return self

    def addAll(self) -> Git:
        """
        Add all changes to the Git staging area.

        Returns:
            Git: The current Git object.
        """
        subprocess.call(["git.exe", "add", "--all"], shell=True, cwd=self.workingDir)
        return self

    def commit(self, comment: str) -> Git:
        """
        Commit the staged changes with a given commit message.

        Args:
            comment (str): The commit message.

        Returns:
            Git: The current Git object.
        """
        subprocess.call(["git.exe", "commit", "-m", f'"{comment}"'], shell=True, cwd=self.workingDir)
        return self

    def clone(self, remoteDir: PurePath) -> Git:
        """
        Clone a remote Git repository into the working directory.

        Args:
            remoteDir (PurePath): The URL or path to the remote Git repository.

        Returns:
            Git: The current Git object.
        """
        subprocess.call(["git.exe", "clone", f'"{remoteDir}"'], shell=True, cwd=self.workingDir)
        return self

    def addSubModule(self, subModuleDir: PurePath) -> Git:
        """
        Add a Git submodule to the repository.

        Args:
            subModuleDir (PurePath): The URL or path to the Git submodule.

        Returns:
            Git: The current Git object.
        """
        subprocess.call(["git.exe", "submodule", "add", f'"{subModuleDir}"'], shell=True, cwd=self.workingDir)
        return self

    def push(self, remoteDir: PurePath) -> Git:
        """
        Push the changes to a remote Git repository.

        Args:
            remoteDir (PurePath): The URL or path to the remote Git repository.

        Returns:
            Git: The current Git object.
        """
        subprocess.call(["git.exe", "push"], shell=True, cwd=self.workingDir)
        return self
