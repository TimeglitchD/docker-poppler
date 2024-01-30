import os
import uuid
import tempfile
import subprocess as sp
from json import JSONEncoder
from werkzeug.utils import secure_filename
from flask import Flask, request, send_file, send_from_directory

class CalledProcessErrorEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

app = Flask(__name__)

@app.route("/")
def index():
    return 'Welcome to timeglitchd/poppler'

@app.route("/inkscape", methods=['POST'])
def inkscape():
    if 'file' not in request.files:
        return {
            'success': False,
            'message': 'file is required.'
        }

    file = request.files['file']
    infile = tempfile.NamedTemporaryFile(suffix='.pdf')
    file.save(infile.name)
    outfile = str(uuid.uuid4())
    os.mkdir(f'./media/{outfile}')
    sp.run(['inkscape', '--export-type=svg', f'--export-filename=./media/{outfile}/output.svg', infile.name], check=True)
    return {
        'images': [f'/media/{outfile}/{i}' for i in os.listdir(f'./media/{outfile}/')]
    }

@app.route("/pdftocairo", methods=['POST'])
def pdftocairo():
    if 'file' not in request.files:
        return {
            'success': False,
            'message': 'file is required.'
        }

    file = request.files['file']
    infile = tempfile.NamedTemporaryFile()
    file.save(infile.name)
    outfile = str(uuid.uuid4())
    os.mkdir(f'./media/{outfile}')
    sp.run(['pdftocairo', '-svg', infile.name, f'./media/{outfile}/output.svg'], check=True)
    return {
        'images': [f'/media/{outfile}/{i}' for i in os.listdir(f'./media/{outfile}/')]
    }

@app.route("/pdfinfo", methods=['POST'])
def pdfinfo():
    if 'file' not in request.files:
        return {
            'success': False,
            'message': 'file is required.'
        }

    file = request.files['file']
    infile = tempfile.NamedTemporaryFile()
    file.save(infile.name)

    output = sp.run(['pdfinfo', infile.name], capture_output=True, check=True)
    return output.stdout

@app.route("/pdftotext", methods=['POST'])
def pdftotext():
    if 'file' not in request.files:
        return {
            'success': False,
            'message': 'file is required.'
        }

    file = request.files['file']
    infile = tempfile.NamedTemporaryFile()
    file.save(infile.name)

    output = sp.run(['pdftotext', infile.name, '-'], capture_output=True, check=True)
    return output.stdout



@app.route('/media/<path:name>')
def download_file(name):
    return send_from_directory('./media/', name)

