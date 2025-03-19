import json

from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def str_into_object(input: str | list) -> dict:
    if isinstance(input, list):
        # Convert list to JSON string
        input = json.dumps(input)
    try:
        return json.loads(input)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {input}") from e
