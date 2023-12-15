import requests, os, re, time, random, string
from colorama import Fore, Style
from supabase import create_client, Client
from supload.uploadsong import usongtosup
from supload.uploadimage import uimagetosup

url = "https://hoalciqrtruvfuaviwjf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvYWxjaXFydHJ1dmZ1YXZpd2pmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NTAzMTg0OSwiZXhwIjoyMDEwNjA3ODQ5fQ.FXle8gUMdz4FlZ30kp3pBGluyVCvICx4Bv_zaySgZek"
supabase: Client = create_client(url, key)

def extract_info(filename):
    global author
    global title
    match = re.match(r'^(.*?) - (.*?)\.mp3$', filename)
    if match:
        author = match.group(1)
        title = match.group(2)
        return author, title
    return None, None
headers = {}
def send(file, randkey):
    filename = None
    songwithoutspaces = title.replace(" ", "%20")
    songwithoutspacesorbracketsp1 = songwithoutspaces.replace("(", "%28")
    songwithoutspacesorbracketsp2 = songwithoutspacesorbracketsp1.replace(")", "%29")
    songwithoutspacesorbracketordashs = songwithoutspacesorbracketsp2.replace("-", "%2D")
    songwithoutspacesorbracketordashsorquote = songwithoutspacesorbracketordashs.replace("'", "%27")
    artistwithoutspace = author.replace(" ", "%20")
    r = requests.get(F"https://sds.xeno.fm/v1/track?title={songwithoutspacesorbracketordashsorquote}&artist={artistwithoutspace}",headers=headers).json()
    img = None
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
                sjhdgg = uname.replace(".png", "")
                os.system(f"mv {filename} {uname}")
                titl = result["title"]
                img = sjhdgg
            else:
                print()
        else:
            print()
    else:
        print()
    if filename is not None:
        uimagetosup(key, filename, randkey)
    usongtosup(key, file, randkey)
    makerecord(title, author, randkey, img)


def makerecord(title, author, randkey, img):
    image_path = f"image-{randkey}"
    song_path = f"song-{randkey}"
    t = title
    a = author
    if img is None:
        image_path = "notfound"
    data = {"title": t, "author": a, "image_path": image_path, "song_path": song_path}
    response = supabase.table('songs').insert([data]).execute()


def main():
    path = "supload/songs"
    totalfiles = 0
    for file in os.listdir(path):
        if file.endswith(".mp3"):
            randkey = ''.join(random.choice(string.ascii_letters) for _ in range(36))
            totalfiles = totalfiles + 1
            extract_info(file)
            print(
                Fore.BLUE + f"[+] Title: {title}\n[+] Author: {author}" + Style.RESET_ALL)
            send(file, randkey)
            os.system(f"cp 'supload/songs/{file}' .")
    return totalfiles


if __name__ == "__main__":
    os.system("sudo clear")
    print(Fore.GREEN + "[!] Running" + Style.RESET_ALL)
    totalfiles = main()
    os.system("sudo clear")
    print(Fore.BLUE + "[!] Cleaning Up Files" + Style.RESET_ALL)
    time.sleep(1)
    os.chdir("/workspaces/imgrepo/supload/songs/")
    os.system("rm *.mp3")
    os.chdir("/workspaces/imgrepo/")
    os.system("rm *.mp3 *.png")
    os.system("sudo clear")
    print(Fore.GREEN + "[+] Finished" + Style.RESET_ALL)
    print(Fore.CYAN + f"[+] Total Songs Found: {totalfiles}" + Style.RESET_ALL)
