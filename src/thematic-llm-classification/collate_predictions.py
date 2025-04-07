import json
from promptflow import tool

@tool
def consolidate_classifications(
    asset: str,
    benefit: str,
    pressure: str,
    valuation: str
) -> str:
    """
    Consolidates classifications from multiple JSON strings into a single JSON string.

    Args:
        asset (str): JSON string containing asset classification.
        benefit (str): JSON string containing benefit classification.
        pressure (str): JSON string containing pressure classification.
        valuation (str): JSON string containing valuation classification.

    Returns:
        str: A JSON string containing the consolidated classifications.
    """

    asset_dict = json.loads(asset)
    benefit_dict = json.loads(benefit)
    pressure_dict = json.loads(pressure)
    valuation_dict = json.loads(valuation)

    combined_output = ""

    for d in [asset_dict, benefit_dict, pressure_dict, valuation_dict]:
        output = d.get("output")
        #need to deal with cases where it is give a list and conv this to a string 
        if isinstance(output, list):
            combined_output += " ".join(str(item) for item in output)
        elif isinstance(output, str):
            combined_output += output

    merged_doc = {
        "output": combined_output
    }

    return json.dumps(merged_doc)
