'''
Response format:
  group_name = 'calibration' | 'short_answer' | 'yes_no' | free_response

  {
    <group name>: [
      (<question>, <answer>)
    ]
  }
'''

questions = {
  "groups": [
    {
      "name": "calibration",
      "label": "Calibration Questions",
      "type": "checkbox",
      "questions": [
        "Yes?",
        "No?"
      ]
    },
    {
      "name": "short_answer",
      "label": "",
      "type": "text",
      "questions": [
        "First Name",
        "Last Name",
        "Maiden Name",
        "Bachelor Name",
        "Title",
        "Suffix",
        "Prefix",
        "Net Worth",
        "Highest Level of Education",
        "Country of Origin",
        "First Language",
        "First Programming language",
        "Favorite OS",
        "First four digits of mother's maiden social security number"
      ]
    },
    {
      "name": "yes_no",
      "label": "",
      "type": "select",
      "questions": [
        {
          "question": "Milk Before or After Cereal?",
          "options": ["Before", "After"]
        },
        {
          "question": "Butter side up or down?",
          "options": ["Up", "Down"]
        }
        
      ]
    },
    {
      "name": "free_response",
      "label": "Free Response",
      "type": "textfield",
      "questions": [
        "Fish Friday?"
      ]
    }
  ]
}