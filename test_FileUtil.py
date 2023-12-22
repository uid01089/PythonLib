from pathlib import Path
from PythonLib.FileUtil import FileOperations


def test1() -> None:
    parentPath = Path("c:\\root")
    childPath = Path("c:/root\\child")

    assert FileOperations.isChild(parentPath, childPath)
