import json
import random
import string

# Function to generate a random string prefix
def generate_random_prefix(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Load the dataset
file_path = 'DatasetGenerator\\IntermediaryFiles\\synthetic_dataset_train.json'
with open(file_path, 'r') as file:
    dataset = json.load(file)

# Function to make the dataset human readable and assign iterative dialogue IDs with a random prefix
def process_dataset(dataset):
    random_prefix = generate_random_prefix()  # Generate a random prefix for this session
    dialogue_number = 1  # Start dialogue numbering from 1
    
    for scenario_group in dataset:
        for scenario in scenario_group["scenarios"]:
            # Assign an iterative dialogue_id with the format: random_prefix_dialoguenumber
            scenario["dialogue_id"] = f"{random_prefix}_{dialogue_number}"
            dialogue_number += 1  # Increment dialogue number for each scenario
    return dataset

# Process the dataset with iterative dialogue IDs
processed_dataset = process_dataset(dataset)

# Save the processed dataset to a new file
processed_file_path = 'DatasetGenerator\\IntermediaryFiles\\processed_synthetic_dataset_train_iterative.json'
with open(processed_file_path, 'w') as file:
    json.dump(processed_dataset, file, indent=2)

