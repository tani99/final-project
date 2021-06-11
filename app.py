import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask import Flask, flash, request, redirect, send_file, render_template, send_from_directory
from werkzeug.utils import secure_filename

from process import process_file

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        'NLP for Education',
        View('Home', 'index'),
        View('PDF to Text', 'pdfToText'),
    )

# ...

UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
Bootstrap(app)
nav.init_app(app)


@app.route("/")
def index():
    return render_template('home.html')

@app.route("/pdfToText", methods=['GET', 'POST'])
def pdfToText():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            text_file = process_file(file)
            text_filename = secure_filename(text_file.filename)
            text_file.save(os.path.join(app.config['PROCESSED_FOLDER'], text_filename))

            print("saved file successfully")
            # send file name as parameter to download
            return redirect('/downloadfile/' + text_filename)
    return render_template('pdf-to-text.html')

# Download API
@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename=filename, as_attachment=True)
    # return render_template('download.html', value=filename)
