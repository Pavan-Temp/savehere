import requests
import json
import base64
import os
from datetime import datetime as day

# Get GitHub access token from environment variable for security
access_token = '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'
if not access_token:
    print("GitHub token is missing. Please set the GITHUB_TOKEN environment variable.")
    exit(1)

# Replace with your GitHub username, repository name, and commit message
username = 'Pavan-Temp'
repository = 'savehere'
commit_message = 'Add file via Flask'

print(f"my key: {access_token}")

def upload_to_github(file_content, file_name):
    base_url = f'https://api.github.com/repos/{username}/{repository}/contents/'
    headers = {'Authorization': f'token {access_token}'}
    file_name = file_name.replace(" ", "")
    
    # Check if the file already exists
    response = requests.get(base_url + file_name, headers=headers)
    
    if response.status_code == 200:
        # File exists, modify the file name by appending a timestamp
        timestamp = str(day.now()).replace(' ', '-').split('.')[0]
        str_temp = file_name.rsplit('.', 1)  # Split at the last dot to preserve multi-part extensions
        file_name = f"{str_temp[0]}_{timestamp}.{str_temp[1]}"
        
        print(f"File with the same name exists. Renamed to {file_name}")
    
    # Proceed with the chunked upload as before
    CHUNK_SIZE = 5 * 1024 * 1024  # 1 MB chunks
    chunks = [file_content[i:i + CHUNK_SIZE] for i in range(0, len(file_content), CHUNK_SIZE)]
    sha = None

    for i, chunk in enumerate(chunks):
        encoded_content = base64.b64encode(chunk).decode('utf-8')
        payload = {
            'message': f'Adding chunk {i+1} of {len(chunks)}',
            'content': encoded_content,
            'branch': 'main'
        }

        if sha:
            payload['sha'] = sha  # Include SHA to continue the file upload

        payload = json.dumps(payload)
        retries = 0
        success = False

        while retries < 3:  # Retry mechanism
            try:
                response = requests.put(base_url + file_name, headers=headers, data=payload, timeout=100)
                if response.status_code in [200, 201]:
                    sha = response.json().get('content', {}).get('sha')
                    print(f"Chunk {i+1} uploaded successfully")
                    success = True
                    break
                else:
                    print(f"Error uploading chunk {i+1}: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error during chunk upload {i+1}: {e}")
            
            retries += 1
            print(f"Retrying chunk {i+1} upload ({retries}/3)")

        if not success:
            raise Exception(f"Failed to upload chunk {i+1} after 3 retries.")

    return True, file_name

def delete_from_github(file_name):
    base_url = f'https://api.github.com/repos/{username}/{repository}/contents/'
    headers = {'Authorization': f'token {access_token}'}
    file_name = file_name.replace(" ", "")

    # Get the file's SHA (necessary for deletion)
    response = requests.get(base_url + file_name, headers=headers)
    if response.status_code == 200:
        sha = response.json().get('sha')
        delete_url = base_url + file_name
        payload = {
            'message': f'Deleting {file_name}',
            'sha': sha,
            'branch': 'main'
        }

        # Attempt to delete the file
        response = requests.delete(delete_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print(f"File {file_name} deleted successfully.")
            return True
        else:
            print(f"Failed to delete file {file_name}: {response.status_code} - {response.text}")
            return False
    else:
        print(f"File {file_name} not found or cannot be accessed: {response.status_code} - {response.text}")
        return False
