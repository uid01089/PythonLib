from __future__ import annotations
from pathlib import PurePath
import subprocess


class Git:
    def __init__(self, workingDir: PurePath) -> None:
        self.workingDir = workingDir

    def init(self) -> Git:
        subprocess.call(["git.exe", "init"], shell=True, cwd=self.workingDir)

    def initBare(self) -> Git:
        subprocess.call(["git.exe", "init", "--bare"], shell=True, cwd=self.workingDir)

    def addAll(self) -> Git:
        subprocess.call(["git.exe", "add", "--all"], shell=True, cwd=self.workingDir)

    def commit(self, comment: str) -> Git:
        subprocess.call(["git.exe", "commit", "-m", f'"{comment}"'], shell=True, cwd=self.workingDir)

    def clone(self, remoteDir: PurePath) -> Git:
        subprocess.call(["git.exe", "clone", f'"{remoteDir}"'], shell=True, cwd=self.workingDir)

    def addSubModule(self, subModuleDir: PurePath) -> Git:
        subprocess.call(["git.exe", "submodule", "add", f'"{subModuleDir}"'], shell=True, cwd=self.workingDir)

    def push(self, remoteDir: PurePath) -> Git:
        subprocess.call(["git.exe", "push"], shell=True, cwd=self.workingDir)
