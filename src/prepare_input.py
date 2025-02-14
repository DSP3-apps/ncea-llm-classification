import csv
import hashlib
import json
import random

import click


def hash_input_to_md5(input: str) -> str:
    json_string = json.dumps(input, sort_keys=True)
    return hashlib.md5((json_string).encode()).hexdigest()

@click.command()
@click.argument('csv_file_path', type=click.Path(exists=True))
@click.argument('output_file_path', type=click.Path())
@click.option('--count', '-c', default=0, help='Number of rows to sample. Default is all rows.')
def csv_to_jsonl(csv_file_path: str, output_file_path: str, count: int = 0) -> None:
    """Convert CSV file to JSONL format with optional random sampling."""
    result = []
    all_rows = []

    with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                all_rows.append(row)
            except UnicodeDecodeError:
                continue
    if count > len(all_rows) or count == 0:
        count = len(all_rows)
    sampled_rows = random.sample(all_rows, count)

    for row in sampled_rows:
        item = {
            'title': row['Title'],
            'altTitle': row['AltTitle'],
            'source': row['Source'],
            'custodian': row['c_custodian'],
            'topics': row['Topics'],
            'keywords': row['Keywords'],
            'abstract': row['Abstract'],
            'lineage': row['Lineage'],
        }
        result.append(json.dumps(item))
    output = '\n'.join(result)

    with open(output_file_path, 'w') as file:
        file.write(output)

if __name__ == '__main__':
    csv_to_jsonl()