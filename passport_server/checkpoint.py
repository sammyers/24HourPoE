from .questions import questions

def evaluate_responses(responses, names, wearing_hat):
  print(responses)
  if wearing_hat:
    return '', True
  return "Because you're not a real buffalo", False
