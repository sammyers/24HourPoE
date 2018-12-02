import requests
def evaluate_answers(responses, name):
    calibration = {'yes':'yes', 'no':'no'}
    points = 0
    for group in responses:
        if group == 'calibration':
            for (question,answer) in responses[group]:
                if question[0] == 'Y':
                    calibration['yes'] = answer
                elif question[1] == 'N':
                    calibration['no'] = answer
        if group == 'short_answer':
            first_name = ""
            last_name = ""
            for (question,answer) in reponses[group]:
                if question == 'First Name':
                    first_name = answer
                elif question == 'Last Name':
                    last_name = answer
                elif question == 'Net Worth':
                    net_worth = 0
                    try:
                        net_worth = int(question)
                    except e:
                        return (False, "Net worth must be an INTEGER")
                
    
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

text = 'hello, and fuck you'
sentiment = get_sentiment(text)
print("string: ", text)
print("sentiment: (", sentiment, ")NEGATIVE")
