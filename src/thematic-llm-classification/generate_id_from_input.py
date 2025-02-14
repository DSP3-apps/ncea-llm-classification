
import hashlib
import json

from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def hash_input_to_md5(input: str) -> str:
    json_string = json.dumps(input, sort_keys=True)
    return hashlib.md5((json_string).encode()).hexdigest()
