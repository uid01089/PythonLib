import re

# This class provides utility functions for string operations.

numberPattern = re.compile('^[-+]?(\\d+(\\.\\d*)?|\\.\\d+)$')


class StringUtil:
    @staticmethod
    def isNubmer(string: str) -> bool:
        # Define a regular expression pattern to match positive/negative integers and floats
        # number_pattern = r'^[-+]?(\d+(\.\d*)?|\.\d+)$'

        # return bool(re.match(number_pattern, string))
        return bool(numberPattern.match(string))

    @staticmethod
    def isBoolean(string: str) -> any:
        state = None

        if string.lower() in ('true', 'on', '1'):
            state = True
        elif string.lower() in ('false', 'off', '0'):
            state = False

        return state
