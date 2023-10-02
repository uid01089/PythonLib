from datetime import datetime

# This class provides utility functions for date and time operations.


class DateTimeUtilities:
    @staticmethod
    def getCurrentDateString() -> str:
        """
        Get the current date and time as a formatted string.

        Returns:
            str: A string representing the current date and time in the format "YYYY-MM-DD-HH-MM-SS".
        """
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        return dt_string
