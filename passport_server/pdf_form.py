import jinja2
import pyqrcode
import io
import base64
import requests
from weasyprint import HTML
from itertools import zip_longest
from pprint import pprint
from .questions import questions

PRINT_URL = 'http://ac314x01.olin.edu/supload/xerox.set'

column_sizes = {
  'calibration': 3,
  'short_answer': 4,
  'yes_no': 6,
  'free_response': 12
}

def group_pairs(pairs, group_size=3):
  return list(zip_longest(*(iter(pairs),) * group_size))

def get_base_64_string(data):
  return base64.b64encode(data).decode('ascii')

def get_question_pair(q, responses, group_name):
  question = q['question'] if type(q) is dict else q
  return (question, responses[group_name][question])

def format_group(group, responses):
  return {
    'name': group['name'],
    'questions': group_pairs([
      get_question_pair(q, responses, group['name'])
      for q in group['questions']
    ], 12 // column_sizes[group['name']]),
    'colspan': column_sizes[group['name']]
  }

def format_responses(responses):
  formatted = [format_group(group, responses) for group in questions['groups']]
  return formatted


def get_qr_code_image(qr_data):
  qr = pyqrcode.create(qr_data)
  stream = io.BytesIO()
  qr.png(stream, scale=4)
  encoded = get_base_64_string(stream.getvalue())
  return encoded

def render_template(**args):
  TEMPLATE_FILE = 'template.html'

  template_loader = jinja2.FileSystemLoader(searchpath='./')
  template_env = jinja2.Environment(loader=template_loader)

  template = template_env.get_template(TEMPLATE_FILE)
  with open('background.png', 'rb') as f:
    background = get_base_64_string(f.read())

  return template.render(background=background, **args)

def html_to_pdf(html):
  doc = HTML(string=html)
  return doc.write_pdf()

def write_to_pdf_file(html, filename):
  with open('test.html', 'w') as f:
    f.write(html)
  pdf = html_to_pdf(html)
  with open(filename, 'wb') as f:
    f.write(pdf)


def get_form_pdf(qr_id, responses):
  qr_image = get_qr_code_image(qr_id)
  html = render_template(qr_image=qr_image, responses=format_responses(responses))
  return html_to_pdf(html)

def network_print(pdf):
  form_data = {
    'RFC1867_FileType': 'PRINT_REQUEST',
    'job_type': 'print',
    'CSRFToken': '316ae97f9e616e7b44a2f36037dd47a6f6fc9a97dd14e9a8ccd1d3c583495f2a1f41e896a0470a970171da0d62ae035cdaa27d32c5f207403477cab8738a83b6'
  }
  files = {
    'test.pdf': io.BytesIO(pdf)
  }
  response = requests.post(PRINT_URL, files=files, data=form_data)

def save_pdf(pdf):
  with open('test.pdf', 'wb') as f:
    f.write(pdf)

if __name__ == '__main__':
  pdf = html_to_pdf(html)
  network_print(pdf)
# write_to_pdf_file(html, 'test.pdf')

# print(group_responses(sample_responses, 3))
