from .questions import questions
import requests
import random

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

def generate_rules():
  rules = {}
  rules['max_wealth'] = random.randint(10000,10000000)
  rules['min_wealth'] = random.randint(1000,10000)
  rules['not_allowed_countries'] = random.sample(["United States", "USA", "US", "Canada", "China", "UK", "England", "Vatican City", "Somalia", "CPRB"], 4)
  rules['not_allowed_os'] = random.sample(["Linux", "Mac", "OSX", "Ubuntu", "Windows", "Gentoo", "Debian"], 4)
  rules['cereal'] = random.choice(['yes','no'])
  rules['butter'] = random.choice(['yes','no'])
  return rules

def maybe_fail(message):
  if random.uniform(0, 1) < 0.8:
    return message, False
  return '', True
  
def evaluate_responses(responses, names, wearing_hat, rules):
  print(responses)
  if wearing_hat:
    return '', True
  calibration = {'yes':'yes', 'no':'no'}
  points = 0
  first_name = ""
  last_name = ""
  for group, questions in responses.items():
    for question, answer in questions.items():
      if group == 'calibration':
        if question[0] == 'Y':
          calibration['yes'] = answer
        elif question[0] == 'N':
          calibration['no'] = answer

      elif group == 'short_answer':
        if question == 'First Name':
          first_name = answer
        elif question == 'Last Name':
          last_name = answer
        elif question == 'Net Worth':
          net_worth = 0
          try:
            net_worth = int(answer)
            if net_worth > rules['max_wealth']:
              return maybe_fail("Net worth out of range")
            elif net_worth < rules['min_wealth']:
              return maybe_fail("You're too poor")
          except e:
            return maybe_fail("Net worth must be an INTEGER")
        elif question == "Country of Origin":
          if answer in rules['not_allowed_countries']:
            return maybe_fail("Buffolonia is not currently accepting Visa applications from your country")
        elif question == "Favorite OS":
          if answer in rules['not_allowed_os']:
            return maybe_fail("Buffolonia thinks your OS is trash")
        elif question == "First four digits of mother's maiden social security number":
          ssn = 0
          try:
            ssn = int(answer)
            if ssn % 2 == 0:
              return maybe_fail("SSN must be an odd number")
          except e:
            return maybe_fail("First four digits of mother's maiden social security number must be an INTEGER")

      if group == "yes_no":
        mapping = {
          "Before": "yes",
          "After": "no",
          "Up": "yes",
          "Down": "no"
        }
        if question == "Milk Before or After Cereal?":
          if calibration[mapping[answer]] == rules['cereal']:
            return maybe_fail("Bufalo does not accept people with such disgusting cereal preferences")
        elif question == "Butter side up or down?":
          if calibration[mapping[answer]] == rules['butter']:
            return maybe_fail("Bufalo does not accept people with such disgusting toast preferences")

      if group=="free_response":
        if question == "Fish Friday?":
          sentiment = get_sentiment(answer)
          if sentiment != -1:
            return maybe_fail("Fish friday response not sufficiently negative")

  if first_name + " " + last_name not in names:
    return maybe_fail("You are not who you say you are")

  if random.uniform(0, 1) > 0.5:
    return maybe_fail("Because you're not a real buffalo")
  return '', True

