class DictUtil:
    # Defining a static method flatDict within the class DictUtil
    @staticmethod
    def flatDict(dictionary: dict, name: str) -> list[tuple]:
        """
        This function takes a dictionary and a string as arguments and returns a list of tuples.
        It flattens the dictionary, i.e., it converts a nested dictionary into a list of tuples
        where each tuple contains a string representing the path to a key in the dictionary and the corresponding value.

        :param dictionary: The input dictionary to be flattened. It should be a dict type.
        :param name: The initial string used in forming the path to a key in the dictionary. It should be a str type.
        :return: A list of tuples, where each tuple contains a string representing the path to a key in the dictionary and the corresponding value.
        """
        # Initialize an empty list to store the tuples
        listOfLines = []
        # Initialize an empty list to use as a stack for storing the dictionaries and their corresponding paths
        stack = []

        # Start by adding the input dictionary and its corresponding path to the stack
        stack.append((dictionary, name))

        # Iterate until the stack is empty
        while len(stack) > 0:
            # Pop a dictionary and its corresponding path from the stack
            currentDic = stack.pop()
            # Iterate over the key-value pairs in the dictionary
            for key, value in currentDic[0].items():
                # If the value is a dictionary, add it and its corresponding path to the stack
                if isinstance(value, dict):
                    stack.append((value, currentDic[1] + "/" + key))
                else:
                    # If the value is not a dictionary, add a tuple containing the path to the key and the value to the list
                    listOfLines.append((currentDic[1] + "/" + key, value))

        # Return the list of tuples
        return listOfLines
