import os
import shutil
import requests
import base64
import argparse
import img2pdf
from bs4 import BeautifulSoup
from tqdm import tqdm

def linkToBase64(link):
    sample_string_bytes = link.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    base64_string = base64_string.replace('=', '')
    return base64_string

def get_bitmoji_links(username):
    init_url = "https://www.snapchat.com/add/" + username
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(init_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        picture_elements = soup.find_all('picture')
        for picture in picture_elements:
            source_element = picture.find('source')
            if source_element:
                srcset = source_element.get('srcset', '')
                if srcset.startswith('https://images.bitmoji.com/3d/avatar/'):                    
                    count = int(srcset[srcset.index('_')+1:-11])
                    part1 = srcset[:srcset.index('_')]
                    part2 = (srcset[-11:])
        return count,part1,part2
    else:
        print("Failed to fetch Bitmoji links. Status code:", response.status_code)
        return []

def download_bitmoji(link, username, i):
    response = requests.get(link)
    if response.status_code == 200:
        with open(username + "/picture" + str(i) + ".jpg", 'wb') as f:
            f.write(response.content)

def func(username):
    print("Downloading Bitmojis...")
    c,p1,p2 = get_bitmoji_links(username)
    bitmojis_links=[]
    for i in range(0, c):
        link = linkToBase64(p1+'_'+str(i)+p2)
        bitmojis_links.append(link)
    print("Total Bitmojis:", c)
    if os.path.exists(username):
        shutil.rmtree(username, ignore_errors=False)
    os.makedirs(username)

    for i, link in enumerate(tqdm(bitmojis_links, desc='Downloading Bitmojis')):
        link2 = "https://cf-st.sc-cdn.net/aps/snap_bitmoji/" + link + "._Fmpng"
        download_bitmoji(link2, username, i)

    os.chdir(username)
    images = [i for i in os.listdir(os.getcwd()) if i.endswith(".jpg")]
    dpix = dpiy = 300
    layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
    with open("../" + username + ".pdf", "wb") as f:
        f.write(img2pdf.convert(images, layout_fun=layout_fun))
    os.chdir("../")
    shutil.rmtree(username, ignore_errors=False)
    print("\t\t\tThank you for using khoji")
    print("\t\t\tPrevious Bitmoji's count is " + str(c))
    print("\t\t\tPrevious Bitmoji's of " + username + " are saved in " + username + ".pdf")

if __name__ == "__main__":
    description = """
            ██╗  ██╗██╗  ██╗ ██████╗      ██╗██╗
            ██║ ██╔╝██║  ██║██╔═══██╗     ██║██║
            █████╔╝ ███████║██║   ██║     ██║██║
            ██╔═██╗ ██╔══██║██║   ██║██   ██║██║
            ██║  ██╗██║  ██║╚██████╔╝╚█████╔╝██║
            ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝
    This script gets all previous Bitmojis and saves them in a PDF file named by username.pdf
    Make a pull request if you want to improve it.
    """
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-u", "--Username", help="To Query the Username")
    args = parser.parse_args()
    print(description)

    if args.Username:
        func(args.Username)
