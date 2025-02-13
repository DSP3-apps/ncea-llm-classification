
import json

from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(asset: str, benefit: str, pressure: str, valuation: str) -> str:
    asset_dict = json.loads(asset)
    benefit_dict = json.loads(benefit)
    pressure_dict = json.loads(pressure)
    valuation_dict = json.loads(valuation)
    
    merged_doc = {
        "asset": asset_dict,
        "benefit": benefit_dict,
        "pressure": pressure_dict,
        "valuation": valuation_dict
    }
    
    return json.dumps(merged_doc)