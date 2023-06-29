from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from docx import Document
import io
from flask_cors import CORS
from bs4 import BeautifulSoup
import re

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/natgit/Documents/Code/Projects/flask-server/instance/db.sqlite3'
db.init_app(app)

# from app import db, Upload
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded {file.filename}'
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def list():
    # docs = db.session.execute(db.select(Upload).order_by(Upload.id)).all()
    docs = Upload.query.all()
    for item in docs:
        print("item", item.filename)

    # pprint("DOCS", vars(docs))
    return render_template('list.html', docs=docs)

@app.route('/parse_doc/<id>', methods=['GET'])
def parse_doc(id):
    print("id --------------------------------------")
    print("id", id)
    doc = Upload.query.filter_by(id=id).first_or_404()
    print("doc --------------------------------------")
    print("doc", doc.filename)
    parsed = read_docx(doc.data)
    print(parsed)
    return render_template('parse_doc.html', doc=doc, parsed=parsed)

def read_docx(data):
    b = io.BytesIO(data)
    for item in b:
        print('item------------------------')
        print(item.decode('iso-8859-1'))
        soup = BeautifulSoup(item, 'html.parser')
        print('Soup item-------------------------')
        print(soup)
        tag = soup.span
        print('Soup span class-------------------------')
        print(tag)
        print('Get ALL Text: -------------------------')
        print(soup.get_text())
        print('For each SPAN: -------------------------')
        for link in soup.find_all('span'):
            print('For each STRING!: -------------------------')
            print(link.string)
        for link in soup.find_all('span'):
            print('For each STRING!: -------------------------')
            print(link.string)
        extract_invoice_to(soup)
# account
# parent_company
# customer_worksite
# phone
# email
def extract_invoice_to(soup):
    print('Extract Invoice To: ----------------------------------')
    invoice_line = None
    invoice_details = []
    invoice_end = None
    for i, span_tag in enumerate(soup.find_all('span')):
        print("i----------------", i)
        print("SPAN TAG-------------------", span_tag.string)
        x = None
        if span_tag.string is not None:
            x = re.search("Invoice To:", span_tag.string)
        if x is not None:
            print("THIS IS THE RIGHT SPAN TAG-----------------", x)
            invoice_line = i
            print("MATCH***************", x)
            print(span_tag.string)
        print("Invoice Line************************", invoice_line)
        print("Invoice End************************", invoice_end)
        if (invoice_line is not None and i > invoice_line and span_tag.string is not None and invoice_end is None):
            print('Details: ----------------------------------')
            invoice_details.append(span_tag.string)
            print(invoice_details)
        if (invoice_line is not None and i > invoice_line and span_tag.string == None and invoice_end is None):
            invoice_end = i
    print('Invoice Details: ----------------------------------')
    print(invoice_details)

@app.route('/api/data')
def get_data():
    data = {'message': 'Hello, world!'}
    return data

if __name__ == '__main__':
    app.run(debug=True)