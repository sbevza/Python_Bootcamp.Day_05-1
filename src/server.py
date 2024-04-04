from flask import Flask, request, render_template_string, redirect, url_for
import os
import mimetypes

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            return redirect(url_for('upload_file'))
        else:
            return 'Non-audio file detected', 400
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string('''<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<ul>
    {% for file in files %}
    <li>{{ file }}</li>
    {% endfor %}
</ul>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
''', files=files)


if __name__ == '__main__':
    app.run(port=8888)
