import os
import glob
import yaml
import re
import pandas as pd

# --- CONFIGURATION ---
# The script assumes it is being run from the root of your project repository.
CORPUS_DIRECTORY = "corpus"
OUTPUT_CSV_FILE = "corpus_metadata.csv"

def parse_md_file(filepath):
    """
    Reads a markdown file and robustly separates YAML front matter from content
    using a regular expression.

    Args:
        filepath (str): The path to the .md file.

    Returns:
        dict: A dictionary containing the parsed metadata, or None on failure.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()
        
        # Use a robust regex to capture YAML and content, flexible with whitespace.
        match = re.match(r'^---\s*(.*?)\s*---\s*(.*)', full_content, re.DOTALL)
        
        if match:
            yaml_content, _ = match.groups()
            metadata = yaml.safe_load(yaml_content)
            
            # Add the filename (without extension) as the 'title' for easy merging later.
            metadata['title'] = os.path.splitext(os.path.basename(filepath))[0]
            return metadata
        else:
            print(f"  - WARNING: Skipping '{filepath}' (no valid YAML front matter found).")
            return None
            
    except Exception as e:
        print(f"  - ERROR: Could not parse file '{filepath}': {e}")
        return None

def generate_metadata_csv(corpus_path, output_file):
    """
    Scans a directory for .md files, parses their YAML front matter,
    and generates a master CSV file.
    """
    all_metadata = []
    
    # Check if the corpus directory exists
    if not os.path.isdir(corpus_path):
        print(f"FATAL ERROR: Corpus directory '{corpus_path}' not found.")
        print("Please run this script from the root of your repository.")
        return

    # Use glob to recursively find all .md files in the corpus directory
    filepaths = glob.glob(f"{corpus_path}/**/*.md", recursive=True)
    
    if not filepaths:
        print(f"WARNING: No '.md' files found in the '{corpus_path}' directory.")
        return
        
    print(f"Found {len(filepaths)} document files. Parsing metadata...")

    for fp in filepaths:
        metadata = parse_md_file(fp)
        if metadata:
            # Ensure the essential columns are present
            if all(key in metadata for key in ['id', 'type', 'attack_vector', 'title']):
                all_metadata.append({
                    'id': metadata['id'],
                    'title': metadata['title'],
                    'type': metadata['type'],
                    'attack_vector': metadata.get('attack_vector', 'null') # Use .get for safety
                })
            else:
                print(f"  - WARNING: Skipping '{fp}' (missing one or more required keys: id, type, attack_vector).")

    if not all_metadata:
        print("Could not extract any valid metadata. Please check the format of your .md files.")
        return

    # Sort the data by the 'id' field for a clean, consistent output file
    all_metadata_sorted = sorted(all_metadata, key=lambda x: x['id'])

    # Create a pandas DataFrame
    df = pd.DataFrame(all_metadata_sorted)

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)
    
    print(f"\nSuccessfully parsed {len(df)} documents.")
    print(f"Master metadata file '{output_file}' has been created/updated successfully.")

if __name__ == "__main__":
    generate_metadata_csv(CORPUS_DIRECTORY, OUTPUT_CSV_FILE)
