import re
from typing import List

# Precompile regular expression patterns for number and indentation matching
numberPattern = re.compile(r'^[-+]?(?:\d+(\.\d*)?|\.\d+)$')
indentPattern = re.compile(r'^[ \t]+', re.MULTILINE)


class StringUtil:
    """
    This class provides utility functions for string operations.
    """

    @staticmethod
    def isNumber(string: str) -> bool:
        """
        Determine if the provided string represents a valid number.

        Args:
            string (str): The string to check.

        Returns:
            bool: True if the string is a valid number, False otherwise.
        """
        return bool(numberPattern.match(string))

    @staticmethod
    def isBoolean(string: str) -> bool | None:
        """
        Determine if the provided string represents a boolean value.

        Args:
            string (str): The string to check.

        Returns:
            bool | None: True if the string is a boolean "True" value, False if it's a boolean "False" value,
                         and None if the string is not a recognized boolean value.
        """
        state: bool | None = None

        if string.lower() in ('true', 'on', '1', 'yes'):
            state = True
        elif string.lower() in ('false', 'off', '0', 'no'):
            state = False

        return state

    @staticmethod
    def dedent(string: str) -> str:
        """
        Remove leading indentation (spaces or tabs) from each line in the provided multi-line string.

        Args:
            string (str): The multi-line string to dedent.

        Returns:
            str: The dedented string.
        """
        return indentPattern.sub("", string)

    @staticmethod
    def extractSubString(multiLine: str, startLine: int, startPos: int, endLine: int, endPos: int) -> str:
        """
        Extracts a substring from a text file based on specified start and end positions.

        :param multiLine: String containing multi lines
        :param start_line: 0-based index of the start line.
        :param start_pos: 0-based index of the start cursor position in the start line.
        :param end_line: 0-based index of the end line.
        :param end_pos: 0-based index of the end cursor position in the end line.
        :return: The extracted substring.
        """

        lines: List[str] = multiLine.split("\n")

        # Verify that the line numbers are within the valid range
        if startLine < 0 or endLine >= len(lines):
            raise ValueError("Line numbers out of range")

        # Verify that the cursor positions are within the valid range for each line
        if startPos < 0 or startPos > len(lines[startLine]):
            raise ValueError("Start position out of range")
        if endPos < 0 or endPos > len(lines[endLine]):
            raise ValueError("End position out of range")

        # If start and end positions are within the same line, return the substring from that line
        if startLine == endLine:
            return lines[startLine][startPos:endPos]

        # Initialize the result string with the part of the first line from start_pos to the end
        result: str = lines[startLine][startPos:]

        # Append full lines between the start and end line
        for line in lines[startLine + 1:endLine]:
            result += line

        # Append the start of the end line up to the end position
        result += lines[endLine][:endPos]

        return result
