import ast
import json
import re
from openai import OpenAI

from dataclasses import dataclass
from typing import List

client = OpenAI(
  organization='org_key',
  api_key='api_key'
)

def dialogue_annotation_init(config, example):
    
    #Dialogue initialisation prompt
    prompt = f"Based on this config: {config}; Generate a MultiWOZ 2.2 annotation for the first dialogue act. Use this formatting structure: \n {example}\n Format it as a json. Output only the json"

    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    answer = completion.choices[0].message.content  

    return(answer)

def dialogue_checker(dialogue):
    
    # Dialogue stopper prompt
    prompt = f'Please answer just "yes" or "no" if "{dialogue}" has reached its end'
    
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        max_tokens=40,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    answer = completion.choices[0].message.content.strip().lower()  # Ensure answer is in lower case and stripped of whitespace

    #print(answer)  # For debugging purposes

    # Determine if the goal was successfully addressed
    if answer == "yes":
        return 1  # The current goal was successfully addressed
    else:
        return 0  # The current goal was not successfully addressed

def diag_continue(diag, config,domain):

    #Dialogue prompt enforcing the conversation history
    prompt= f'''Knowing this topic plan {config} \n I have this MultiWoZ 2.2 dialogue act:\n {diag}
Please generate the next dialogue act starting from it. The domain is {domain}. Format it as a json. Return only the json. '''
    
    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    answer = completion.choices[0].message.content  

    return(answer)

def generate_init(domain):

    file_path = 'IntermediaryFiles\\formatted_output.json'

    
    with open(file_path, 'r') as file:
        file_content = json.load(file)

    
    content = json.loads(file_content["content"])
    diag_list = []

    # Iterating through each pair in the 'pairs' list
    for pair in content["pairs"]:

        #print(json.dumps(pair, indent=2)) # For debugging reasons

        # Structure example for annotated dialogue
        example = '''{
  "dialogue_id": "SOME_ID",
  "turns": [
    {
      "turn_id": 1,
      "speaker": "participant1",
      "utterance": "",
      "frames": [
        {
          "service": "",
          "slots": [],
          "actions": [
            {
              "act": "OFFER",
              "slot": null,
              "values": [
                "Check guest in",
                "Offer additional services"
              ]
            }
          ],
          "state": {
            "active_intent": "Check guest in",
            "slot_values": {
              "Availability of rooms": []
            }
          }
        }
      ]
    }
  ]
}'''
        config = json.dumps(pair, indent=2)
        initiated_dialogue = dialogue_annotation_init(config, example)



        lines = initiated_dialogue.split('\n')

        # Remove the first and last lines
        lines_without_first_and_last = lines[1:-1]

        # Join the remaining lines back into a string
        dialogue_string = '\n'.join(lines_without_first_and_last)
        end_check = 0
        end_check_counter =0
        while end_check == 0:
            try:
                dialogue_string = json.loads(dialogue_string)
                print("JSON loaded successfully.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                dialogue_string = None

            diag = diag_continue(dialogue_string, config, domain)

            test_string_cleaned = diag[7:-3]

            # Ensure no leading or trailing whitespace
            test_string_cleaned = test_string_cleaned.strip()

            # Parsing the JSON data to a Python object
            try:
                data = json.loads(test_string_cleaned)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                data = None

            # Appending the new turn to the 'turns' list in the initial data
            dialogue_string["turns"].append(data)

            dialogue_string = json.dumps(dialogue_string, indent=4)

            end_check_counter+=dialogue_checker(dialogue_string)
            if end_check_counter == 5:
                end_check=99

        diag_list.append(dialogue_string)

        print("--------------------------")

    file_path = 'IntermediaryFiles\\list_contents.json'
    with open(file_path, 'w') as file:

        json_object = {"scenarios": diag_list}
        json.dump(json_object, file, indent=4)