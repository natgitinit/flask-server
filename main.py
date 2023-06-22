from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from docx import Document
import io

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
    # document = Document(data)
    document = Document(io.BytesIO(data)).getvalue().split()
    table = document.tables[0]
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
    # docText = b'\n\n'.join(
    #     paragraph.text for paragraph in document.paragraphs
    # )
    # docText.read()
    # docText = '\n\n'.join([paragraph.text.encode('utf-8') for paragraph in document.paragraphs])
    # b = io.BytesIO(doc.data).getvalue().split()
    # b = io.BytesIO(data).getvalue().split()
    # result = str(b).encode('ascii')
    # for item in b:
    #     print('item------------------------')
    #     print(item.decode('iso-8859-1'))
    # print(result)
    # print("b --------------------------------------")
    # print(b)
    # fileobj = open(result)
    # fo = open(result, "w+")
    # print ("Name of file: ", fo.name)
    # print ("Opening mode: ", fo.mode)
    # wo = fo.write("filename")

read_docx

if __name__ == '__main__':
    app.run(debug=True)