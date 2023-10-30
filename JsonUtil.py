import json
import pathlib
from typing import Dict

# https://docs.python.org/3/library/json.html


class JsonUtil:
    @staticmethod
    def loadJson(path: pathlib.PurePath) -> Dict:
        """
        This function loads a JSON file from a specified path and returns it as a dictionary.

        Parameters:
        path (pathlib.PurePath): The path where the JSON file is located.

        Returns:
        dict: A dictionary that contains the data from the JSON file.
        """

        # Open the file in read mode.
        with open(path, 'r') as json_file:
            # Use 'json.load' to load the file content into a dictionary.
            json_data = json.load(json_file)

        # Return the dictionary.
        return json_data

    @staticmethod
    def saveJson(path: pathlib.PurePath, object: Dict) -> None:
        """
        This function saves a dictionary object as a JSON file at a specified path.

        Parameters:
        path (pathlib.PurePath): The path where the JSON file will be saved.
        object (Dict): The dictionary object that will be saved as a JSON file.

        Returns:
        None
        """

        # Open the file in write mode. If the file does not exist, it will be created.
        # 'encoding' parameter is set to 'utf-8' to support all languages.
        with open(path, 'w', encoding='utf-8') as f:
            # 'json.dump' method is used to write the dictionary object to the file.
            # 'ensure_ascii' parameter is set to False to ensure that the file can store non-ASCII characters.
            # 'indent' parameter is set to 4 to pretty print the JSON with 4 spaces indentation.
            json.dump(object, f, ensure_ascii=False, indent=4)
