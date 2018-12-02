import jinja2
import pyqrcode
import io
import base64
import requests
from weasyprint import HTML
from itertools import zip_longest

PRINT_URL = 'http://ac314x01.olin.edu/supload/xerox.set'

sample_responses = [
  ('First Name', 'Sam'),
  ('Last Name', 'Myers'),
  ('Maiden Name', 'Gamgee'),
  ('Bachelor Name', 'Jackson'),
  ('Prefix', 'Rabbi'),
  ('Suffix', 'Esq.')
]

def group_pairs(pairs, group_size):
  return list(zip_longest(*(iter(pairs),) * group_size))

def get_base_64_string(data):
  return base64.b64encode(data).decode('ascii')

def group_responses(responses):
  return group_responses(responses, 3)


def get_qr_code_image(qr_data):
  qr = pyqrcode.create(qr_data)
  stream = io.BytesIO()
  qr.png(stream, scale=6)
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
  html = render_template(qr_image=qr_image, responses=group_responses(responses))
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

if __name__ == '__main__':
  pdf = html_to_pdf(html)
  network_print(pdf)
# write_to_pdf_file(html, 'test.pdf')

# print(group_responses(sample_responses, 3))
