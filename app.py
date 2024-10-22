from flask import Flask, render_template, request, session, send_file, send_from_directory
from git_repo import upload_to_github, delete_from_github  # Ensure these functions are imported correctly
from sql_operations import retrive, insert, delete_file
from io import BytesIO
import mimetypes
import os
import requests
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def main():
    return render_template('key.html')

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/check_shit', methods=['POST', 'GET'])
def check_shit():
    session['username'] = request.form['key']
    print("Session username:", session['username'])
    
    data = retrive(session['username'])
    if data == 'new':
        return render_template('index.html', user=session['username'])
    
    return render_template('index.html', user=session['username'], data=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        return render_template('index.html', status='User not logged in')

    print("Session username:", session['username'])
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part in the form!'

        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file!'
        
        # Check the file size (100MB = 100 * 1024 * 1024 bytes)
        file.seek(0, os.SEEK_END)  # Move pointer to the end to get size
        file_size = file.tell()
        file.seek(0)  # Reset file pointer after reading size

        if file_size > 100 * 1024 * 1024:
            return 'File exceeds the maximum allowed size of 100MB!'
        
        file_content = file.read()
        file_name = file.filename

        try:
            success,file_name = upload_to_github(file_content, file_name)

            if success:
                insert(session['username'], file_name)
                return render_template('index.html', status='uploaded', user=session['username'], data=retrive(session['username']))
            else:
                return render_template('index.html', status='Not uploaded/File Name Already exists', user=session['username'], data=retrive(session['username']))
        except Exception as e:
            print(f"Upload error: {e}")
            return render_template('index.html', status='Error uploading file', user=session['username'], data=retrive(session['username']))

@app.route('/download', methods=['GET', 'POST'])
def download_file():
    file_name = request.form["file_name"]
    print("Attempting to download file:", file_name)
    file_url = f"https://raw.githubusercontent.com/Pavan-Temp/savehere/main/{file_name}"
    
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an error for bad responses
            
        # Use the filename from the URL or from the request
        filename = os.path.basename(file_url)
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        file_content = BytesIO(response.content)
        return send_file(file_content, mimetype=mime_type, as_attachment=True, download_name=filename)
        
    except requests.RequestException as e:
        print(f"Error fetching file: {e}")
        return render_template('index.html', status='Unable to Download', user=session['username'], data=retrive(session['username']))

@app.route('/fuck_off', methods=['GET', 'POST'])
def fuck_off():
    file_name = request.form["file_name"]
    result = delete_file(session['username'], file_name)
    
    if result:
        result = delete_from_github(file_name)
        if result:
            return render_template('index.html', status='Removed', user=session['username'], data=retrive(session['username']))
    
    return render_template('index.html', status='Unable to Remove', user=session['username'], data=retrive(session['username']))

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for development
