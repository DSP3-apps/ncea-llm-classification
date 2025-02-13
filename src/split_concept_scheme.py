import click
import rdflib
from rdflib.namespace import RDF, SKOS


@click.command()
@click.argument("input_file")
@click.argument("output_prefix")
def split_concept_scheme(input_file, output_prefix):
    g = rdflib.Graph()
    g.parse(input_file, format="ttl")


    for concept_schemes in g.subjects(RDF.type, SKOS.ConceptScheme):
        for top_concept in g.objects(concept_schemes, SKOS.hasTopConcept):

            query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

CONSTRUCT {{
    ?collection a skos:Collection ;
                skos:member ?topConcept ;
                skos:member ?descendant .
    ?descendant ?p ?o .
    ?topConcept ?p2 ?o2 .
}}
WHERE {{
    {{
        BIND(<{top_concept}> as ?topConcept)
        ?descendant a skos:Concept ;
                    skos:broader+ ?topConcept .
        ?ontology a skos:ConceptScheme ;
                    skos:hasTopConcept ?topConcept .
        ?descendant ?p ?o .
        ?topConcept ?p2 ?o2 .

        BIND(BNODE(STR(?topConcept)) AS ?collection)

        VALUES ?collectionType {{ skos:Collection }}
        VALUES ?memberProp {{ skos:member }}
    }}
}}
"""
            output_name  = f"{output_prefix}_{str(top_concept).split('/')[-1]}.ttl"
            collection_graph = g.query(query)
            collection_graph.serialize(destination=output_name, format="ttl")
            print(f"Created {output_name}")


if __name__ == "__main__":
    split_concept_scheme()
