from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
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
    print("id", id)
    doc = Upload.query.filter_by(id=id).first_or_404()
    print("doc", doc.filename)
    parsed = read_docx(doc)
    return render_template('parse_doc.html', doc=doc, parsed=parsed)

def read_docx(doc):
    b = io.BytesIO(doc.data).getvalue()
    # b.getvalue()
    # result = b.decode('UTF-8')
    result = str(b)
    return result
    # return "\n".join(result)

read_docx

if __name__ == '__main__':
    pprint('after db.create_all()')
    app.run(debug=False)