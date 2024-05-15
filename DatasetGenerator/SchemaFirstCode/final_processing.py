import json

def final_formatting():
    # Load the JSON data from the uploaded file
    file_path = 'IntermediaryFiles\\formatted_list_contents.json'
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Reformatting process: consolidating all turns into a single array under each scenario
    for scenario in data["scenarios"]:
        new_turns = []
        for turn in scenario["turns"]:
            # Skip over NoneType objects in the turns array
            if turn is None:
                continue
            # Some turns might be wrapped in an extra layer due to incorrect structuring
            if "dialogue_id" in turn and "turns" in turn:
                new_turns.extend(turn["turns"])
            else:
                new_turns.append(turn)
        scenario["turns"] = new_turns

    # Saving the reformatted JSON to a new file
    reformatted_file_path = 'IntermediaryFiles\\reformatted_scenarios.json'
    with open(reformatted_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    reformatted_file_path