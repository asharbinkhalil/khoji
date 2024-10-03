import os
import shutil
import requests
import argparse
from bs4 import BeautifulSoup  # Make sure to install BeautifulSoup
from tqdm import tqdm


def get_count(username):
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
                if srcset.startswith('https://cf-st.sc-cdn.net/3d/render/'):
                    count = srcset.split('_')[-1].split('-')[0]
                    bid = srcset.split('/')[-1].split('-')[1].split('_')[0]
        return count, bid
    else:
        print("Failed to fetch Bitmoji links. Status code:", response.status_code)
        return []

def download_bitmoji(link, username, i):
    response = requests.get(link)
    if response.status_code == 200:
        with open(f"{username}/picture{i}.jpg", 'wb') as f:
            f.write(response.content)

def func(username):
    print("Downloading Bitmojis...")
    c, bid = get_count(username)
    bitmojis_links = []
    for i in range(1, int(c)):
        bitmojis_links.append(f'https://images.bitmoji.com/3d/avatar/201714142-{bid}_{i}-s5-v1.webp')
        bitmojis_links.append(f'https://images.bitmoji.com/3d/avatar/582513516-{bid}_{i}-s5-v1.webp')
        bitmojis_links.append(f'https://images.bitmoji.com/3d/avatar/452520973-{bid}_{i}-s5-v1.webp')

    print("Total Bitmojis:", c)

    if os.path.exists(username):
        shutil.rmtree(username, ignore_errors=False)
    os.makedirs(username)

    for i, link in enumerate(tqdm(bitmojis_links, desc='Downloading Bitmojis')):
        download_bitmoji(link, username, i)

    # Create a Markdown file to display images
    markdown_file_path = f"{username}.md"
    with open(markdown_file_path, "w") as md_file:
        md_file.write(f"# Bitmojis for {username}\n\n")
        for i in range(1, len(bitmojis_links) + 1):
            md_file.write(f"![Bitmoji {i}](./{username}/picture{i}.jpg)\n")

    print("\t\t\tThank you for using khoji")
    print("\t\t\tPrevious Bitmoji's count is " + str(c))
    print("\t\t\tPrevious Bitmoji's of " + username + " are saved in " + markdown_file_path)

if __name__ == "__main__":
    description = """
            ██╗  ██╗██╗  ██╗ ██████╗      ██╗██╗
            ██║ ██╔╝██║  ██║██╔═══██╗     ██║██║
            █████╔╝ ███████║██║   ██║     ██║██║
            ██╔═██╗ ██╔══██║██║   ██║██   ██║██║
            ██║  ██╗██║  ██║╚██████╔╝╚█████╔╝██║
            ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝
    This script gets all previous Bitmojis and saves them in a Markdown file named by username.md
    Make a pull request if you want to improve it.
    """
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-u", "--Username", help="To Query the Username")
    args = parser.parse_args()
    print(description)

    if args.Username:
        func(args.Username)
