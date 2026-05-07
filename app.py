import os
import time
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import filetype

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg"}
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE = 1024*1024*MAX_FILE_SIZE_MB
UPLOAD_COOLDOWN_SECONDS = 3
upload_timestamps = {}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def on_cooldown(ip: str) -> tuple[bool, float]:
    last_upload = upload_timestamps.get(ip)
    if last_upload is None:
        return False, 0.0
    elapsed = time.time() - last_upload
    remaining = UPLOAD_COOLDOWN_SECONDS - elapsed
    return remaining > 0.1, max(remaining, 0.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file_to_upload' not in request.files:
        return "No file part in the request"
    
    client_ip = request.remote_addr
    cooldown, remaining = on_cooldown(client_ip)
    if(cooldown):
    	return f"Please wait {remaining} seconds before uploading"    
    
    file = request.files['file_to_upload']

    if file.filename == '':
        return "No selected file"

    if file:
    	# negiranje path traversala
        filename = secure_filename(file.filename)
        
        # extension provera
        name, ext = os.path.splitext(file.filename)
        if not ext and (ext.lower() not in ALLOWED_EXTENSIONS):
        	return f"File '{filename}' doesnt have an allowed extension"
        	
        # content-type provera
        if file.content_type not in ALLOWED_MIME_TYPES:
        	return f"File '{filename}' doesnt have an allowed content type"    
        
        # header provera
        header = file.stream.read(512)
        file.stream.seek(0)
        kind = filetype.guess(header)
        
        if kind is None or kind.mime not in ALLOWED_MIME_TYPES:
        	return f"File '{filename}' doesnt have an allowed header value"
        
        # size provera
        file.stream.seek(0, os.SEEK_END)
        file_size = file.stream.tell()
        file.stream.seek(0)
        
        if file_size > MAX_FILE_SIZE:
        	return f"File '{filename}' doesnt have an allowed size"
        
        #cuvanje fajla i cuvanje uspesnog vremena
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        upload_timestamps[client_ip] = time.time()
        return f"File '{filename}' uploaded successfully!"

if __name__ == '__main__':
    app.run(debug=False)
