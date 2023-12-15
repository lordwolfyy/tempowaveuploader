import mimetypes
import os
import requests
import sys

def usongtosup(api_key, fpath,randkey):
    object_name = f"song-{randkey}"

    # Set the correct MIME type for the file
    mimetype, _ = mimetypes.guess_type(fpath)
    if not mimetype:
        mimetype = 'application/octet-stream'

    # Read the file data
    file_path = f"supload/songs/{fpath}"
    with open(file_path, 'rb') as file:
        file_data = file.read()  # Read the entire file into memory

    # Construct the headers for the POST request
    headers = {
        'apikey': api_key,
        'authorization': f'Bearer {api_key}',
        'Content-Type': f'multipart/form-data; boundary=boundarystring',
    }

    # Construct the multipart form-data request body
    boundary = 'boundarystring'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="cacheControl"\r\n\r\n'
        f'3600\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name=""; filename="{object_name}"\r\n'
        f'Content-Type: {mimetype}\r\n\r\n'
    )
    payload = body.encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

    # Construct the URL for the POST request
    url = f'https://hoalciqrtruvfuaviwjf.supabase.co/storage/v1/object/songs/{object_name}'

    # Send the POST request using the requests library
    response = requests.post(url, data=payload, headers=headers)

    # Check the response
    if response.status_code == 200:
        print(f'File {object_name} uploaded successfully.')
    else:
        print(f'Failed to upload {object_name}. Status code: {response.status_code}, Response: {response.text}')
 