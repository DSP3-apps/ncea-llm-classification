
import json

from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def format_predictions(collated_predictions: str) -> str:
    """
    Formats the output by combining the given ID with the collated predictions and optionally includes the catalogue entry.

    Args:
        id (str): The unique identifier for the entry.
        collated_predictions (str): A JSON string containing the collated predictions.
        catalogue_entry (str): The original catalogue entry.
        debug (bool, optional): If True, includes the catalogue entry in the output. Defaults to False.

    Returns:
        str: A JSON string containing the formatted output.
    """

    collated_predictions = json.loads(collated_predictions)["output"]

    return json.dumps(collated_predictions)