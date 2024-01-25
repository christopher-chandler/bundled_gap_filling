import json
import re
from typing import List, Optional, Union


class WikiData:
    """
    A class for processing and retrieving data from a JSON file containing wiki information.
    """

    def __init__(self, incoming_file: str, categories: str):
        """
        Initialize the WikiData object.

        Parameters:
        - incoming_file (str): The path to the input JSON file.
        """
        self.incoming_file = incoming_file
        self.categories = categories

    def read_in_wiki(self) -> List[dict]:
        """
        Read the content of the JSON file.

        Returns:
        - List[dict]: A list of dictionaries containing wiki data.
        """
        try:
            with open(self.incoming_file) as infile:
                data = json.load(infile)
            return data
        except FileNotFoundError:
            print(f"File not found: {self.incoming_file}")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {self.incoming_file}")
            return []

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
        category_result = [
            categories[c] for c in categories if category_type in c.lower()
        ]
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

    def save_as_one_file(self) -> None:
        """
        Save text data from the specified category to a text file.

        Reads data from the JSON file based on the specified category,
        extracts text content, and saves it to a text file named 'results.txt'.

        The saved file is located in the '../../data/save_wiki_text/' directory.

        Returns:
        - None
        """
        categories = self.categories
        save_file = open(
            "../../data/incoming_text_data/wiki_data_results.txt", mode="w+"
        )

        for text in wiki_data.get_data_by_categories(categories):
            t = text.get("text")
            document = t.split("\n")
            for doc in document[1:]:
                sen = doc.replace("\n", "")

                doc = sen.split(".")

                for row in doc:
                    if len(row) > 1:
                        save_file.write(row.strip() + "\n")


if __name__ == "__main__":
    pass
