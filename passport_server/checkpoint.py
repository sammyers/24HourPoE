from .questions import questions
import requests

def get_sentiment(text):
    url = "http://text-processing.com/api/sentiment/"
    data = {'text':text}
    r = requests.post(url = url, data = data)
    data = r.json()
    if data['label'] == 'neg':
        return -1
    elif data['label'] == 'pos':
        return 1
    return 0

def evaluate_responses(responses, names, wearing_hat, rules):
  print(responses)
  if wearing_hat:
    return '', True
  calibration = {'yes':'yes', 'no':'no'}
    points = 0
    for group in responses:
        if group == 'calibration':
          for question in responses[group]:
            answer = responses[group][question]
            if question[0] == 'Y':
              calibration['yes'] = answer
            elif question[1] == 'N':
              calibration['no'] = answer
        if group == 'short_answer':
          first_name = ""
          last_name = ""
          for question in reponses[group]:
            answer = responses[group][question]
            if question == 'First Name':
              first_name = answer
            elif question == 'Last Name':
              last_name = answer
            elif question == 'Net Worth':
              net_worth = 0
              try:
                net_worth = int(answer)
                if net_worth > rules['max_wealth']:
                  return "Net worth out of range", False
                elif net_worth < rules['min_wealth']:
                  return "You're too poor", False
              except e:
                return "Net worth must be an INTEGER", False
            elif question == "Country of Origin":
              if answer not in rules['allowed_countries']:
                return "Buffolonia is not currently accepting Visa applications from your country",False
            elif question == "Favorite OS":
              if answer not in rules['allowed_os']:
                return "Buffolonia thinks your OS is trash", False
            elif question == "First four digits of mother's maiden social security number":
              ssn = 0
              try:
                ssn = int(answer)
                if ssn % 2 == 0:
                  return "SSN must be an odd number", False
              except e:
                return "First four digits of mother's maiden social security number must be an INTEGER", False
            if first_name + " " + lastname != name:
              return "You are not who you say you are", False
            
        if group == "yes_no":
          for question in reponses[group]:
            answer = responses[group][question]
            if question == "Milk Before or After Cereal?":
              if calibration[answer] == rules['cereal']:
                return "Bufalo does not accept people with such disgusting cereal preferences", False
            elif question == "Butter side up or down?":
              if calibration[answer] == rules['butter']:
                return "Bufalo does not accept people with such disgusting toast preferences", False
        if group=="free_response":
          for question in repsonses[group]:
            answer = responses[group][question]
            if question == "Fish Friday?":
              sentiment = get_sentiment(answer)
              if sentiment != -1:
                return "Fish friday response not sufficiently negative", False
              
                
  return "Because you're not a real buffalo", False

