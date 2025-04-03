import json

from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
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

    # Process each dictionary and add output if it exists, if it does not exist, skip it. 
    # This is done to avoid KeyError if the key does not exist in the dictionary.
    dict_outputs = ""
    for d in [asset_dict, benefit_dict, pressure_dict, valuation_dict]:
        try:
            dict_outputs += d["output"]
        except KeyError:
            pass
    
    merged_doc = {
        "output": dict_outputs
    }
    
    return json.dumps(merged_doc)
