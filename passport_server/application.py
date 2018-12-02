from flask import Flask, jsonify, request
from .questions import questions
from .pdf_form import get_form_pdf, network_print

app = Flask(__name__)

def format_responses(responses):
  # do some stuff here
  return responses

@app.route('/questions')
def get_questions():
  return jsonify(questions)

@app.route('/print-form', methods=['POST'])
def print_form():
  json = request.get_json()
  pdf = get_form_pdf(json.get('qrId'), json.get('responses'))
  network_print(pdf)

@app.route('/check-application')
def check_application():
  return
