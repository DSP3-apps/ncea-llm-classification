# NCEA Ontology Processing Tool

This tool processes the NCEA Natural Capital vocabulary and converts it into various semantic web formats for use in classification and knowledge representation tasks.

## Prerequisites

- Python 3.12.6+ with required packages installed from `requirements.txt`
- Docker installed and running
- Excel file containing the NCEA Natural Capital vocabulary

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure Docker is running on your system

## Processing Workflow

The workflow consists of three main steps:

### 1. Prepare the Ontology Data

```bash
python ontology_utils.py prepare [input_path] [-o/--out OUTPUT_PATH]
```

This command processes the Excel file containing the NCEA ontology and outputs a cleaned CSV file.

**Parameters:**
- `input_path`: Path to the Excel file (default: `./NCEA Natural Capital vocab for NCEA Search.xlsx`)
- `-o/--out`: Output CSV file path (default: `./ncea_ontology.csv`)

**Example:**
```bash
python ontology_utils.py prepare "/path/to/vocabulary.xlsx" -o "cleaned_ontology.csv"
```

### 2. Populate the DuckDB Database

```bash
python ontology_utils.py populate [input_path] [db_path]
```

This command loads the CSV ontology file into a DuckDB database for faster querying and processing.

**Parameters:**
- `input_path`: Path to the CSV file (default: `./ncea_ontology.csv`)
- `db_path`: Path to the DuckDB database file (default: `./ncea_ontology.duckdb`)

**Example:**
```bash
python ontology_utils.py populate "cleaned_ontology.csv" "ontology_database.duckdb"
```

### 3. Serialize the Ontology

```bash
python ontology_utils.py serialize -m MAPPING_FILE -p PROPERTIES_FILE -f FORMAT -o OUTPUT_FILE
```

This command materializes the ontology using Ontop, converting the database into a specified RDF format.

**Parameters:**
- `-m/--mapping`: Mapping file (must end with .obda)
- `-p/--properties`: Properties file (must end with .properties)
- `-f/--format`: Output file format. Available options:
  - `rdfxml`: RDF/XML format
  - `turtle`: Turtle format
  - `ntriples`: N-Triples format
  - `nquads`: N-Quads format
  - `trig`: TriG format
  - `jsonld`: JSON-LD format
- `-o/--output`: Output file path

**Example:**
```bash
python ontology_utils.py serialize -m ncea_ontology.obda -p ncea_ontology.properties -f turtle -o ncea_ontology_full.ttl
```

## Why This Process?

The process transforms the NCEA Natural Capital vocabulary from an Excel format into standardized semantic web formats:

1. **Data Preparation**: The first step cleans the raw Excel data, removing tabs, non-printable characters, and standardizing the column names.

2. **Database Storage**: Loading the data into DuckDB provides an efficient storage mechanism that can be easily queried using SQL and integrated with Ontop.

3. **Semantic Web Conversion**: The final step uses Ontop to convert the relational data into various RDF formats, allowing the ontology to be used with semantic web technologies, knowledge graphs, and linked data applications.

This conversion enables the NCEA vocabulary to be used in classification systems, semantic search engines, and other applications that require standardized knowledge representation.

## Notes

- Docker is required for running Ontop in the serialization step
- The process automatically downloads the DuckDB JDBC driver when needed
- All file paths can be relative to the current directory or absolute paths

## Todo

- Implement the ontology splitting into collections from topConcepts down to the leaf nodes