class Hysteresis:
    def __init__(self, lowLimit: float, upLimit: float) -> None:
        """
        Initializes a Hysteresis object with specified lower and upper limits.

        Args:
            lowLimit (float): The lower threshold value.
            upLimit (float): The upper threshold value.
        """
        self.lowLimit = lowLimit
        self.upLimit = upLimit
        self.value = False

    def setValue(self, value: float) -> bool:
        """
        Sets the value of the Hysteresis based on the input value.

        Args:
            value (float): The input value to compare with thresholds.

        Returns:
            bool: True if the value is above the upper limit, False if below the lower limit.
        """
        if value > self.upLimit:
            self.value = True
        elif value < self.lowLimit:
            self.value = False
        else:
            pass  # Value is within the hysteresis range, no change
        return self.value
