import requests
import os
import re
import json
import time
import random
import string
import mimetypes
import urllib

from supabase import create_client, Client
from supload.uploadsong import usongtosup
from supload.uploadimage import uimagetosup
import sys
# Replace with your Supabase URL and API key
url = "https://hoalciqrtruvfuaviwjf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvYWxjaXFydHJ1dmZ1YXZpd2pmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NTAzMTg0OSwiZXhwIjoyMDEwNjA3ODQ5fQ.FXle8gUMdz4FlZ30kp3pBGluyVCvICx4Bv_zaySgZek"


supabase: Client = create_client(url, key)
aefsjlgbkjdg = None
try:
    aefsjlgbkjdg = sys.argv[1]
except:
    print()
resp = supabase.table('songs').select("*").execute()
print(resp)
if aefsjlgbkjdg != None:
    sys.exit()

def upimage(file, filenam, randkey, filename):
    filename2 = filename.split('-')[-1].strip()
    
    uimagetosup(key, filenam, "images",filename2 ,randkey)

def upsong(filename, randkey, file):
    usongtosup(key, file, "songs",filename ,randkey)

def extract_info(filename):
    global author
    global title

    match = re.match(r'^(.*?) - (.*?)\.mp3$', filename)
    if match:
        author = match.group(1)
        title = match.group(2)
        return author, title
    return None, None

headers = {
    # Add your headers here if needed
}

def send(file, randkey):
    songwithoutspaces = title.replace(" ","%20")
    songwithoutspacesorbracketsp1 = songwithoutspaces.replace("(","%28")
    songwithoutspacesorbracketsp2 = songwithoutspacesorbracketsp1.replace(")","%29")
    songwithoutspacesorbracketordashs = songwithoutspacesorbracketsp2.replace("-","%2D")
    songwithoutspacesorbracketordashsorquote = songwithoutspacesorbracketordashs.replace("'","%27")
    artistwithoutspace = author.replace(" ","%20")
    print(f"https://sds.xeno.fm/v1/track?title={songwithoutspacesorbracketordashsorquote}&artist={artistwithoutspace}")
    r = requests.get(f'https://sds.xeno.fm/v1/track?title={songwithoutspacesorbracketordashsorquote}&artist={artistwithoutspace}', headers=headers).json()

    img = None  # Initialize img to None

    if 'result' in r:
        result = r["result"]
        if 'covers' in result:
            covers = result["covers"]
            if 'medium' in covers:
                uneed = covers["medium"]
                os.system(f"wget {uneed}")
                time.sleep(0.1)
                filename = uneed.split('/')[-1]
                uname = f"{filename}.png"
                sjhdgg = uname.replace(".png","")
                os.system(f"mv {filename} {uname}")
                titl = result["title"]
                upimage(title, sjhdgg,randkey, file)
                upsong(title, randkey, file)
                img = sjhdgg  # Set img to the image file name
            else:
                print("Medium cover not found in response.")
        else:
            print("Covers not found in response.")
    else:
        print("Result not found in response.")

    makerecord(title, randkey, author, img)


def makerecord(title, randkey, author, img):
    
    x = title.replace(" ","")
    b = urllib.parse.quote(x)
    

    # Generate the image path based on the format 'image-{title}-{randkey}.png'
    image_path = f'image-{b}-{randkey}'
    song_path = f'song-{b}-{randkey}'
    if img == None:
        image_path = "notfound"

    # Define the data to be inserted
    data = {"title": title, "author": author, "image_path": image_path, "song_path": song_path}

    # Insert the record into the "songs" table
    response = supabase.table('songs').insert([data]).execute()
def main():
    path = "supload/songs/"
    totalfiles = 0
    
    for file in os.listdir(path):
        if file.endswith(".mp3"):
            randkey = ''.join(random.choice(string.ascii_letters) for _ in range(6))
            totalfiles = totalfiles + 1
            print(f"Total Files Found: {totalfiles}")
            extract_info(file)
            send(file, randkey)
            os.system(f"cp 'supload/songs/{file}' .")
if __name__ == "__main__":
    main()