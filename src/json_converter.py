#!/usr/bin/env python3
import json
import jsonlines
import sys
import re

def clean_string(value):
    """Clean the string by handling common formatting issues."""
    # Replace escaped newlines and tabs correctly
    value = value.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
    
    # Replace double backslashes with a single backslash
    value = value.replace("\\\\", "\\")
    
    # Remove extra spaces (normalize to single spaces)
    value = re.sub(r'\s+', ' ', value)
    
    # Strip leading/trailing whitespace
    value = value.strip()
    
    # Remove single quotes at the start and end if present
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    
    # Convert all single quotes to double quotes
    value = value.replace("'", '"')
    
    # Escape unescaped double quotes inside the string
    value = re.sub(r'(?<!\\)"', r'\"', value)
    
    return value

def clean_data(data):
    """Recursively clean strings in the data (whether list or dict)."""
    if isinstance(data, dict):
        return {key: clean_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    else:
        return clean_string(data)

def convert_to_jsonl(input_file, output_file):
    """Convert a JSON file to properly formatted JSONL using jsonlines and clean strings."""
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Clean the data before writing to JSONL
        cleaned_data = clean_data(data)

        # Write to JSONL using jsonlines
        with jsonlines.open(output_file, mode='w') as writer:
            if isinstance(cleaned_data, list):
                # If it's a list, write each item as a separate line
                for item in cleaned_data:
                    writer.write(item)
            else:
                # If it's a single object, write it as one line
                writer.write(cleaned_data)

    except json.JSONDecodeError:
        print(f"Error: {input_file} does not contain valid JSON.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input_file output_file")
        sys.exit(1)
    
    convert_to_jsonl(sys.argv[1], sys.argv[2])
    print(f"Converted {sys.argv[1]} to {sys.argv[2]}")