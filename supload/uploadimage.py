import mimetypes
import os
import requests

def uimagetosup(api_key, fpath, randkey):
    image_name = f"image-{randkey}"
    mimetype, _ = mimetypes.guess_type(fpath)
    if not mimetype:
        mimetype = 'image/jpeg'

    # Read the file data
    file_path = f"{fpath}.png"
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
        f'Content-Disposition: form-data; name=""; filename="{image_name}"\r\n'
        f'Content-Type: {mimetype}\r\n\r\n'
    )
    payload = body.encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

    # Construct the URL for the POST request
    url = f'https://hoalciqrtruvfuaviwjf.supabase.co/storage/v1/object/images/{image_name}'

    # Send the POST request using the requests library
    response = requests.post(url, data=payload, headers=headers)
