import tempfile
import urllib.request
from enum import Enum
from pathlib import Path

import click
import docker
import duckdb
import pandas


def process_xlsx_ncea_ontology(file_path: Path) -> pandas.DataFrame:
    """Process NCEA ontology from Excel file and rename columns.

    This function reads an Excel file containing NCEA ontology data, validates its structure,
    and renames columns to a standardized format. The file must have a sheet named 'Original Ontology'
    with exactly 9 columns in a specific order representing three levels of taxonomy
    (ID, Term, Definition for each level).

    Args:
        file_path (Path): Path to the Excel file containing NCEA ontology.

    Returns:
        pandas.DataFrame: DataFrame containing the NCEA ontology data with validated structure.

    Raises:
        ValueError: If the Excel file doesn't contain the expected columns in the exact order:
                   L1 ID, L1 Term, L1 Definition, L2 ID, L2 Term, L2 Definition,
                   L3 ID, L3 Term, L3 Definition.
    """
    df = pandas.read_excel(file_path, sheet_name="Original Ontology")

    # Define column mapping dictionary
    column_mapping = {
        "L1 ID": "l1_id",
        "L1 Term": "l1_term",
        "L1 Definition": "l1_definition",
        "L2 ID": "l2_id",
        "L2 Term": "l2_term",
        "L2 Definition": "l2_definition",
        "L3 ID": "l3_id",
        "L3 Term": "l3_term",
        "L3 Definition": "l3_definition",
    }

    # Validate columns match expected keys
    if list(df.columns) != list(column_mapping.keys()):
        raise ValueError(
            "Excel file must contain columns in exact order: "
            + ", ".join(column_mapping.keys())
        )

    # Rename columns using mapping
    df = df.rename(columns=column_mapping)
    return df


def clean_ontology(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Clean the ontology DataFrame by removing tabs and non-printable ASCII characters from all string columns.

    Args:
        df (pandas.DataFrame): Input DataFrame containing the ontology data

    Returns:
        pandas.DataFrame: Cleaned DataFrame with tabs replaced by spaces and non-printable ASCII characters removed from all string/object columns
    """
    # Convert tabs to spacers and remove non-printable ASCII chars from all string columns
    # Convert tabs to spaces, strip whitespace, and remove non-printable ASCII chars from all string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = (
            df[col]
            .str.replace("\t", " ")
            .str.strip()
            .str.replace(r"[^ -~]+", "", regex=True)
        )

    return df


def output_ontology(df: pandas.DataFrame, output_path: Path):
    """
    Write a DataFrame to a CSV file at the specified path.

    Args:
        df (pandas.DataFrame): The DataFrame to be written to CSV
        output_path (Path): The file path where the CSV should be saved

    Returns:
        None

    Note:
        The DataFrame is saved without the index column
    """
    df.to_csv(output_path, index=False)


def load_ontology_to_duckdb(
    file_path: Path = Path("./ncea_ontology.csv"),
    db_path: Path = Path("./ncea_ontology.duckdb"),
):
    """Load CSV ontology file into DuckDB database.

    Args:
        file_path (Path): Path to CSV file containing ontology data
        db_path (Path): Path to DuckDB database file
    """

    conn = duckdb.connect(str(db_path))
    conn.execute("DROP TABLE IF EXISTS ncea_ontology")
    conn.execute(f"CREATE TABLE ncea_ontology AS SELECT * FROM '{file_path}'")
    conn.close()


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    default="./NCEA Natural Capital vocab for NCEA Search.xlsx",
)
@click.option(
    "-o",
    "--out",
    type=click.Path(path_type=Path),
    default="./ncea_ontology.csv",
    help="Output CSV file path",
)
def prepare(input_path: Path, out: Path):
    """Process XLSX ontology file and output cleaned CSV."""
    df = process_xlsx_ncea_ontology(input_path)
    df = clean_ontology(df)
    output_ontology(df, out)


@cli.command()
@click.argument(
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    default="./ncea_ontology.csv",
)
@click.argument(
    "db_path", type=click.Path(path_type=Path), default="./ncea_ontology.duckdb"
)
def populate(input_path: Path, db_path: Path):
    """Load ontology CSV into DuckDB database."""
    load_ontology_to_duckdb(input_path, db_path)


class OutputFormat(str, Enum):
    RDFXML = "rdfxml"
    TURTLE = "turtle"
    NTRIPLES = "ntriples"
    NQUADS = "nquads"
    TRIG = "trig"
    JSONLD = "jsonld"


@cli.command()
@click.option(
    "-m",
    "--mapping",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Mapping file (must end with .obda)",
)
@click.option(
    "-p",
    "--properties",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Properties file (must end with .properties)",
)
@click.option(
    "-f",
    "--format",
    required=True,
    type=click.Choice([f.value for f in OutputFormat]),
    help="Output file format (one of: rdfxml, turtle, ntriples, nquads, trig, jsonld)",
)
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(path_type=Path),
    help="Output file path",
)
def serialize(mapping: Path, properties: Path, format: str, output: Path):
    """Materialize ontology using OnTop."""
    if not str(mapping).endswith(".obda"):
        raise click.BadParameter("Mapping file must end with .obda")
    if not str(properties).endswith(".properties"):
        raise click.BadParameter("Properties file must end with .properties")

    # Create temporary directory for DuckDB JDBC driver
    tmp_dir = Path(tempfile.mkdtemp())
    jdbc_path = tmp_dir / "duckdb-jdbc.jar"

    # Download JDBC driver if it doesn't exist
    if not jdbc_path.exists():
        urllib.request.urlretrieve(
            "https://repo1.maven.org/maven2/org/duckdb/duckdb_jdbc/1.2.1/duckdb_jdbc-1.2.1.jar",
            jdbc_path,
        )

    client = docker.from_env()

    volumes = {
        str(mapping.parent.absolute()): {"bind": "/opt/ontop/input", "mode": "rw"},
        str(jdbc_path): {"bind": "/opt/ontop/jdbc/duckdb_jdbc-1.2.1.jar", "mode": "ro"},
    }

    client.containers.run(
        "ontop/ontop",
        entrypoint="",
        command=[
            "ontop",
            "materialize",
            "-m",
            mapping.name,
            "-p",
            properties.name,
            "-f",
            format,
            "-o",
            output.name,
        ],
        volumes=volumes,
        working_dir="/opt/ontop/input",
        remove=True,
        user="root",
    )


if __name__ == "__main__":
    cli()
