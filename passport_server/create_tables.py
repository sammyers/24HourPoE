import sqlite3

DB_NAME = 'bufalonia.db'

def create_tables():
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()
  cur.execute('''
              CREATE TABLE IF NOT EXISTS applicants
              (id text PRIMARY KEY, responses text)
              ''')
  conn.commit()
  conn.close()

if __name__ == '__main__':
  create_tables()
  print('Tables created.')
