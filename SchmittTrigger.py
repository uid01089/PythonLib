class SchmittTrigger:
    """
    A class to implement a Schmitt Trigger which is a type of comparator with two different threshold voltage levels.
    It is used to convert an analog input signal to a digital output signal.
    """

    def __init__(self, debounceValue: float) -> None:
        """
        Initializes the SchmittTrigger class with the given debounce value.

        Parameters:
            debounceValue (float): The debounce value which is used to prevent the Schmitt Trigger from rapidly toggling.
        """
        self.debounceValue = debounceValue
        self.oldResult = False  # A variable to store the previous result
        self.threshold = 0  # The threshold value at which the output toggles

    def setValue(self, value: float, threshold: float) -> bool:
        """
        Sets the value and threshold for the Schmitt Trigger and determines the output based on these values and the debounce value.

        Parameters:
            value (float): The input value.
            threshold (float): The threshold value.

        Returns:
            bool: The output of the Schmitt Trigger.
        """

        # Reset DebounceValue in case threshold was changed
        if self.threshold != threshold:
            debounceValue = 0
        else:
            debounceValue = self.debounceValue

        if self.oldResult:
            # If the previous result was True (ON), we have to reach threshold - debounceValue to toggle the output
            if value < (threshold - debounceValue):
                self.oldResult = False
        else:
            # If the previous result was False (OFF), we have to reach threshold + debounceValue to toggle the output
            if value > (threshold + debounceValue):
                self.oldResult = True

        return self.oldResult  # Return the output of the Schmitt Trigger
