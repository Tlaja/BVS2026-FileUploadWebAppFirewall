# WAF for File Uploads
A whitelisting firewall for web application uploads  
**Authors:** Strahinja Grujić 11/23ri - Uroš Ivanković 6/23ri

---

## Setup and Running

```bash
user@computer~$ git clone [repository-link]
user@computer~$ cd BVS2026-FileUploadWebAppFirewall
user@computer~$ python3 -m venv venv
user@computer/BVS2026-FileUploadWebAppFirewall$ source venv/bin/activate
(venv) user@computer/BVS2026-FileUploadWebAppFirewall$ pip install flask
(venv) user@computer/BVS2026-FileUploadWebAppFirewall$ pip install filetype
(venv) user@computer/BVS2026-FileUploadWebAppFirewall$ python3 app.py
```
The webapp will then be running on localhost:5000 and will be accessible through a browser
## Modifying
To change the allowed extensions and types change the these lists on line 11-12 in app.py
```python
ALLOWED_EXTENSIONS = {".extension1", ".extension2"}
ALLOWED_MIME_TYPES = {"mime_type1", "mime_type2"}
```
To change the allowed size of files change this parameter on line 13 in app.py
```python
MAX_FILE_SIZE_MB = 20
```
To lower the time interval between uploads change this parameter on line 15 in app.py
```python
UPLOAD_COOLDOWN_SECONDS = 3
```
