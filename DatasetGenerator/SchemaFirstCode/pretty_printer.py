import json

def human_readable():
    # Load the original JSON file
    file_path = 'IntermediaryFiles\\list_contents.json'
    formatted_file_path = 'IntermediaryFiles\\formatted_list_contents.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    formatted_scenarios = []

    for scenario_str in data['scenarios']:

        scenario_json = json.loads(scenario_str)
        formatted_scenarios.append(scenario_json)

    with open(formatted_file_path, 'w') as file:
        json.dump({"scenarios": formatted_scenarios}, file, indent=4, ensure_ascii=False)

    print(f"Formatted JSON has been saved to: {formatted_file_path}")
