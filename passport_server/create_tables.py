import sqlite3

DB_NAME = 'bufalonia.db'

def create_tables():
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()
  cur.execute('''
              CREATE TABLE IF NOT EXISTS applicants
              (id text PRIMARY KEY, responses text)
              ''')
  cur.execute('''
              CREATE TABLE IF NOT EXISTS rules
              (id integer PRIMARY KEY, rule_set text)
              ''')
  conn.commit()
  conn.close()

if __name__ == '__main__':
  create_tables()
  print('Tables created.')
