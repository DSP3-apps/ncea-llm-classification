import ast
import json
from promptflow.core import tool

@tool
def fix_alt_title(input_data: str) -> str:
    """
    Fixes the altTitle field and invalid escape sequences in the input data.
    Expects input_data as a JSON string and returns a JSON string.
    """
    # Preprocess the input to fix invalid escape sequences
    input_data = input_data.replace("\\ n", "\\n")

    # Parse the input JSON string into a dictionary
    try:
        input_data = json.loads(input_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {input_data}") from e

    # Fix altTitle if it's a string
    if "altTitle" in input_data and isinstance(input_data["altTitle"], str):
        if input_data["altTitle"].startswith("[") and input_data["altTitle"].endswith("]"):
            # Handle string representation of a list
            input_data["altTitle"] = ast.literal_eval(input_data["altTitle"])
        else:
            # Handle comma-separated string to cover for differeing input variations
            input_data["altTitle"] = [item.strip() for item in input_data["altTitle"].split(",")]

    # Serialize the updated dictionary back to a JSON string
    return json.dumps(input_data)