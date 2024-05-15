import argparse
import json
import yaml

from SchemaFirstCode.dialogue_init import diag_init
from SchemaFirstCode.initiate_diag import generate_init
from SchemaFirstCode.pretty_printer import human_readable
from SchemaFirstCode.final_touches import final_formatting

SUPPORTED_DOMAINS = {"hotel", "train"}

def parse_args():
    parser = argparse.ArgumentParser(description="Process input for the data pipeline.")
    parser.add_argument('-y', '--yaml', type=str, help="Path to the YAML dataset configuration file.")
    parser.add_argument('-l', '--list', nargs='+', help="Domains to generate datasets.")
    parser.add_argument('-r', '--repetitions', type=int, default=1, help="Number of dialogues for dataset generation.")
    return parser.parse_args()

def load_config(args):
    if args.yaml:
        try:
            with open(args.yaml, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    elif args.list:
        return args.list
    else:
        print("No input provided.")
        exit(1)

def process_domain(domain, repetitions, max_retries = 3):
    for _ in range(int(repetitions/4)):
        if domain not in SUPPORTED_DOMAINS:
            print(f"{domain}: Warning, this domain is not supported. The annotation will not match the standard format.")
            continue

        diag_init(domain)
        print("Config files done")
        # Retry loop for generate_init
        for attempt in range(max_retries):
            try:
                print("Attempting to generate dialogue")
                generate_init(domain)
                print("Dialogue generation successful")
                break  # Break out of the loop if successful
            except Exception as e:
                print(f"Error during dialogue generation: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                else:
                    print("Maximum retries reached, moving on to next step.")
                    
        print("Dialogue generation done")
        human_readable()
        print("Human-readable conversion done")
        final_formatting()
        print("Final formatting done")
        
        append_dialogue_to_synthetic_dataset(domain)

def append_dialogue_to_synthetic_dataset(domain):
    source_file_path = 'IntermediaryFiles\\reformatted_scenarios.json'
    target_file_path = f'IntermediaryFiles\\synthetic_dataset_{domain}.json'
    
    with open(source_file_path, 'r') as source_file:
        source_data = json.load(source_file)
    
    try:
        with open(target_file_path, 'r+') as target_file:
            try:
                existing_data = json.load(target_file)
            except json.JSONDecodeError:
                existing_data = []
            existing_data.append(source_data)
            target_file.seek(0)
            json.dump(existing_data, target_file)
            target_file.truncate()
    except FileNotFoundError:
        with open(target_file_path, 'w') as target_file:
            json.dump([source_data], target_file)

def main():
    args = parse_args()
    config = load_config(args)

    for domain in config:
        process_domain(domain, args.repetitions)

if __name__ == "__main__":
    main()
