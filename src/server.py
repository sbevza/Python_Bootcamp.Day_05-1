from flask import Flask, request, render_template_string, redirect, url_for, jsonify
import os
import mimetypes

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    mimetype, _ = mimetypes.guess_type(filename)
    return mimetype in ['audio/mpeg', 'audio/ogg', 'audio/wav']


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
    files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
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


@app.route('/api/files', methods=['GET'])
def list_files_api():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    return jsonify(files)


@app.route('/api/upload', methods=['POST'])
def upload_file_api():
    if 'file' not in request.files:
        return jsonify({"error": "File is missing"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Filename is missing"}), 400
    if file and allowed_file(file.filename):
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Non-audio file detected"}), 400


if __name__ == '__main__':
    app.run(port=8888)
