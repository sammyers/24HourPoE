from flask import Flask, jsonify, request, g
from uuid import uuid1
import sqlite3
import json
from .questions import questions
from .pdf_form import get_form_pdf, network_print, save_pdf
from .create_tables import DB_NAME
from .checkpoint import evaluate_responses, generate_rules

app = Flask(__name__)

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DB_NAME)
  return db

def query_db(query, args=(), one=False):
  conn = get_db()
  cur = conn.cursor()
  cur.execute(query, args)
  conn.commit()
  rv = cur.fetchall()
  return (rv[0] if rv else None) if one else rv

def save_responses(id, responses):
  response_string = json.dumps(responses)
  query_db(
    'INSERT INTO applicants (id, responses) VALUES (?, ?)',
    (id, response_string)
  )

def retrieve_responses(id):
  result = query_db(
    'SELECT responses FROM applicants WHERE id = ?',
    (id,),
    True
  )
  return json.loads(result[0]) if result else None

def retrieve_rules():
  result = query_db(
    'SELECT rule_set FROM rules WHERE id = 1',
    (),
    True
  )
  return json.loads(result[0]) if result else None

def save_rules(rules):
  rules_string = json.dumps(rules)
  query_db(
    'INSERT OR REPLACE INTO rules (id, rule_set) VALUES (1, ?)',
    (rules_string,)
  )

@app.route('/questions')
def get_questions():
  return jsonify(questions)

@app.route('/print-form', methods=['POST'])
def print_form():
  json = request.get_json()
  responses = json.get('responses')
  qrId = str(uuid1())
  save_responses(qrId, responses)

  pdf = get_form_pdf(qrId, responses)
  network_print(pdf)
  # save_pdf(pdf)
  return 'Printed', 200

@app.route('/responses')
def get_responses():
  id = request.args.get('id')
  responses = retrieve_responses(id)
  return jsonify(responses)

@app.route('/check-application', methods=['POST'])
def check_application():
  json = request.get_json()
  responses = retrieve_responses(json.get('qrId'))
  rules = retrieve_rules()
  print(responses)
  print(rules)
  reason, admitted = evaluate_responses(
    responses,
    json.get('names'),
    json.get('wearingHat'),
    rules
  )
  return jsonify({ 'admitted': admitted, 'reason': reason })

@app.route('/rules')
def get_rules():
  return jsonify(retrieve_rules())

@app.route('/change-rules', methods=['POST'])
def change_rules():
  rules = generate_rules()
  save_rules(rules)
  return 'New rules saved', 200

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()
