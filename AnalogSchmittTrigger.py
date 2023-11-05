class AnalogSchmittTrigger:
    """
    This class implements an Analog Schmitt Trigger.
    A Schmitt Trigger is a comparator circuit that incorporates positive feedback.
    What this means is that the Schmitt Trigger has two distinct threshold voltage levels.
    """

    def __init__(self, delta: float) -> None:
        """
        Initializes the AnalogSchmittTrigger object with the specified delta value.
        :param delta: The difference between the upper and lower threshold levels.
        """
        self.delta = delta
        self.lastValidValue = 0.0  # The last valid value that was within the limits

    def getFilteredValue(self, currentValue: float) -> float:
        """
        Filters the current value based on the upper and lower threshold levels.
        If the current value is outside these limits, it is considered valid and replaces the last valid value.
        :param currentValue: The value to be filtered.
        :return: The filtered value.
        """
        upperLimit = self.lastValidValue + self.delta  # Calculate the upper threshold level
        lowerLimit = self.lastValidValue - self.delta  # Calculate the lower threshold level

        # If the current value is outside the threshold levels, update the last valid value
        if (currentValue >= upperLimit) or (currentValue <= lowerLimit):
            self.lastValidValue = currentValue

        # Return the last valid value
        return self.lastValidValue
