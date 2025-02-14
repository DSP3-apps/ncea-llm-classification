
import json

from promptflow import tool
from rdflib import Graph
from rdflib.query import ResultRow


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool

def fill_predictions(predictions: str, asset: str, valuation: str, benefit: str, pressure: str) -> list:
    # Load and parse the TTL files
    g = Graph()
    g.parse(data=asset, format="turtle")
    g.parse(data=valuation, format="turtle")
    g.parse(data=benefit, format="turtle") 
    g.parse(data=pressure, format="turtle")

    # Parse predictions JSON
    preds = json.loads(predictions)["output"]
    output = preds.copy()

    # Helper function to check if notation is top concept
    def is_top_concept(notation):
        query = f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        ASK {{
            ?s skos:notation "{notation}" ;
                a skos:Concept ;
                skos:topConceptOf ?scheme .
        }}
        """
        return bool(g.query(query))

    # For each prediction
    for pred in preds:
        notation = pred["notation"]
        
        # Skip if top concept
        if is_top_concept(notation):
            continue
            
        # Find broader concept notation
        query = f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?broader_notation
        WHERE {{
            ?concept skos:notation "{notation}" .
            ?concept skos:broader ?broader .
            ?broader skos:notation ?broader_notation .
        }}
        """
        
        results = g.query(query)
        for row in results:
            if not isinstance(row, ResultRow):
                continue
            broader_notation = str(row[0])
            
            # Check if broader not already in predictions
            if not any(p["notation"] == broader_notation for p in output):
                # Add broader concept
                output.append({
                    "notation": broader_notation,
                    "justification": "This term was imputed from a narrower classification."
                })

    return output
