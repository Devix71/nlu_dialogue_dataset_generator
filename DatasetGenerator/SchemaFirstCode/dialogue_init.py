import json
import os
from openai import OpenAI


def diag_init(domain):
  client = OpenAI(
    organization='org_key',
    api_key='api-key'
  )

  # Schema generation prompt
  generator_prompt1 = f'Please write me 1 pair of custom instructions for the participants to a task-oriented dialogue taking place in {domain} scenario. Format it as a json, have multiple goals per participant per pair, which they want to achieve in the conversation and what information they posses. Participants in the same pair shouldn\'t have the same number of goals or informations. Specify the roles of the participants.'
  generator_prompt2 = '''Format it as such 
  {
  "properties": {
    "pairs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "participant1": {
            "type": "object",
            "properties": {
              "role": { "type": "string" },
              "goals": {
                "type": "array",
                "items": { "type": "string" }
              },
              "information": { "type": "string" }
            },
            "required": ["role", "goals", "information"]
          },
          "participant2": {
            "type": "object",
            "properties": {
              "role": { "type": "string" },
              "goals": {
                "type": "array",
                "items": { "type": "string" }
              },
              "information": { "type": "string" }
            },
            "required": ["role", "goals", "information"]
          }
        },
        "required": ["participant1", "participant2"]
      }
    }
  },
  "required": ["pairs"]
}'''
  generator_prompt = generator_prompt1+generator_prompt2


  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    temperature=1,
    response_format= { "type": "json_object" },
    messages=[
      {"role": "user", "content": generator_prompt}
    ]
  )

  # Capture the JSON response
  json_data = completion.choices[0].message.json()

  # Parse the string into a JSON object
  parsed_json = json.loads(json_data)

  # Pretty print the JSON object
  pretty_json = json.dumps(parsed_json, indent=4)

  # Directory path where the file will be saved
  directory_path = 'IntermediaryFiles'

  # Ensure the directory exists
  os.makedirs(directory_path, exist_ok=True)

  # File path
  file_path = os.path.join(directory_path, 'formatted_output.json')

  with open(file_path, 'w') as file:
      file.write(pretty_json)