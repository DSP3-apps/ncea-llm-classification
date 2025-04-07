import json
import re
from rdflib import Graph
from promptflow import tool

@tool
def process_notations(predictions: str, ttl_for_notations: str) -> str:
    """
    Processes notations in predictions by:
    1. Correcting format (replacing hyphens with underscores)
    2. Validating against TTL files to remove invalid predictions
    Args:
    predictions (str): JSON string containing prediction data.
    ttl_for_notations (str): Content of the asset TTL file.
    Returns:
    str: JSON string with corrected and validated predictions.
    """
    
    # Parse the input JSON
    try:
        data = json.loads(predictions)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON input in predictions")
    
    # Error #1 fix: Handle different possible JSON structures
    output_list = []
    if isinstance(data, dict) and "output" in data:
        if isinstance(data["output"], list):
            output_list = data["output"]
        else:
            # Handle case where output is not a list
            output_list = [data["output"]]
    elif isinstance(data, list):
        # If the root is already a list
        output_list = data
    else:
        raise ValueError("Invalid structure: Expected 'output' key with list value or direct list")
    
    #Format Correction - Replace hyphens with underscores in notations
    for item in output_list:
        if isinstance(item, dict) and "notation" in item:
            item["notation"] = item["notation"].replace("-", "_")
    
    #Load and extract valid notations from TTL files
    valid_notations = extract_notations_from_ttl(ttl_for_notations)
    
    # Validation - Keep only predictions with valid notations
    valid_predictions = []
    for prediction in output_list:
        if isinstance(prediction, dict) and "notation" in prediction:
            if prediction["notation"] in valid_notations:
                valid_predictions.append(prediction)
    
    # Reconstruct the JSON with processed predictions
    processed_data = {"output": valid_predictions}
    
    # Return the processed JSON as a string
    return json.dumps(processed_data)

def extract_notations_from_ttl(ttl_data: str) -> set:
    """
    Extracts valid notation values from TTL data using multiple approaches.
    Args:
    ttl_data (str): Content of a TTL file.
    Returns:
    set: Set of valid notation strings from the TTL data.
    """
    notations = set()  # Using set to avoid duplicates
    
    # Approach 1: Use RDFLib (more accurate but might fail on malformed TTL)
    try:
        g = Graph()
        g.parse(data=ttl_data, format="turtle")
        
        # Query for all notation values
        query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?notation
        WHERE {
          ?s skos:notation ?notation .
        }
        """
        results = g.query(query)
        
        # Add all notation values to our set
        for row in results:
            notation_value = str(row[0])
            notations.add(notation_value)
    except Exception as e:
        # If RDFLib parsing fails, fall back to regex approaches
        print(f"RDFLib parsing failed: {str(e)}")
    
    # If no notations found via RDFLib, try regex approaches
    if not notations:
        # Approach 2: Look for patterns like <http://example.com/lvl2_001>
        url_pattern = r'<([^>]+)/([^>]+)>'
        matches = re.finditer(url_pattern, ttl_data)
        for match in matches:
            # Extract the portion after the last slash
            notation = match.group(2)
            # If notation is valid (starts with lvl and contains underscore)
            if notation.startswith('lvl') and '_' in notation:
                notations.add(notation)
    
    # Approach 3: Direct search for lvl patterns if still no results
    if not notations:
        lvl_pattern = r'lvl\d+_\d+'
        matches = re.finditer(lvl_pattern, ttl_data)
        for match in matches:
            notations.add(match.group(0))
    
    return notations