from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def read_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()