from __future__ import annotations
from typing import Any, Callable, List, Optional

from PythonLib.JOptional import JOptional
from PythonLib.Stream import Stream


class TreeElement:
    def __init__(self, this: Any, getChildsOpStr: str) -> None:
        self.this = this
        self.getChildsOpStr = getChildsOpStr
        self.getChildsOp: Callable = None

        try:
            self.getChildsOp = getattr(this, getChildsOpStr)
        except AttributeError:
            print(f"Method '{getChildsOpStr}' not found")

    def getChilds(self) -> List[TreeElement]:

        if self.getChildsOp:
            return Stream(list(self.getChildsOp())) \
                .map(lambda element: TreeElement(element, self.getChildsOpStr)) \
                .collectToList()

        return []

    def getAllElements(self) -> List[Any]:
        elements: List[Any] = []
        elements.append(self.this)

        for child in self.getChilds():
            elements = elements + child.getAllElements()

        return elements


class TreeStream:
    def __init__(self, rootElement: TreeElement) -> None:
        self.rootElement = rootElement

    def toStream(self) -> Stream:
        return Stream(self.rootElement.getAllElements())
