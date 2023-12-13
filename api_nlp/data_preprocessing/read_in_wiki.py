import json
import re
from typing import List, Optional, Union


class WikiData:
    """
    A class for processing and retrieving data from a JSON file containing wiki information.
    """

    def __init__(self, incoming_file: str):
        """
        Initialize the WikiData object.

        Parameters:
        - incoming_file (str): The path to the input JSON file.
        """
        self.incoming_file = incoming_file

    def read_in_wiki(self) -> List[dict]:
        """
        Read the content of the JSON file.

        Returns:
        - List[dict]: A list of dictionaries containing wiki data.
        """
        with open(self.incoming_file) as infile:
            data = json.load(infile)
        return data

    def get_data_by_categories(self, category_type: str) -> List[dict]:
        """
        Get data from the JSON file based on a specified category.

        Parameters:
        - category_type (str): The category type to filter data.

        Returns:
        - List[dict]: A list of dictionaries containing data from the specified category.
        """
        categories = {
            c: item
            for item in self.read_in_wiki()
            for c in item.get("categories", [])
            if c
        }
        category_result = [categories[c] for c in categories if category_type in c.lower()]
        return category_result

    def get_data_by_id(self, id: Union[int, str]) -> Optional[dict]:
        """
        Get data from the JSON file based on a specified ID.

        Parameters:
        - id (Union[int, str]): The ID to search for in the data.

        Returns:
        - Optional[dict]: A dictionary containing data for the specified ID, or None if not found.
        """
        data = self.read_in_wiki()
        return next((file for file in data if file.get("id") == id), None)

    def remove_punc(self, text: str) -> str:
        """
        Remove punctuation from the input text.

        Parameters:
        - text (str): The input text with punctuation.

        Returns:
        - str: The input text with punctuation removed.
        """
        return re.sub(r"[^\w\s]", "", text)


if __name__ == "__main__":
    file_path = (
        "/Users/christopherchandler/code_repos/christopher-chandler/Python/"
        "nlp/rub/bundled_gap_filling/data/wiki_data/simple_wiki_en_01_319188.json"
    )
    wiki_data = WikiData(incoming_file=file_path)

    for i in wiki_data.get_data_by_categories("white"):
        print(i.get("categories"))
