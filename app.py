import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file_to_upload' not in request.files:
        return "No file part in the request", 400
    
    file = request.files['file_to_upload']

    if file.filename == '':
        return "No selected file", 400

    if file:
        # Sanitize the filename
        filename = secure_filename(file.filename)
        # Save the file to our folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"File '{filename}' uploaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)
