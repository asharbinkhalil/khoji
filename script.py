import os,shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests,base64
import argparse

def linkToBase64(link):
    sample_string_bytes = link.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    base64_string=base64_string.replace('=', '')
    return base64_string

def func(username):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    #driver.set_window_position(-10000,0)

    initURL="https://www.snapchat.com/add/"+username
    isExist = os.path.exists(username)
    if isExist:
        shutil.rmtree(username, ignore_errors=False)
    os.makedirs(username)
    driver.get(initURL)
    l=driver.find_element(By.CSS_SELECTOR, "picture[class='css-15e7yeh']")
    l=l.find_element(By.CSS_SELECTOR, "source")
    link = l.get_attribute("srcset")
    count=int(link[link.index('_')+1:-11])
    part1=link[:link.index('_')]
    part2=(link[-11:])
    
    for i in range(0,count):
        link=linkToBase64(part1+'_'+str(i)+part2)
        link2="https://cf-st.sc-cdn.net/aps/snap_bitmoji/"+link+"._Fmpng"
        response = requests.get(link2)
        if response.status_code == 200:
            with open(username+"\picture"+str(i)+".jpg", 'wb') as f:
                f.write(response.content)
        
    driver.close()
    
if __name__== "__main__":
    description = """



            ██╗  ██╗██╗  ██╗ ██████╗      ██╗██╗
            ██║ ██╔╝██║  ██║██╔═══██╗     ██║██║
            █████╔╝ ███████║██║   ██║     ██║██║
            ██╔═██╗ ██╔══██║██║   ██║██   ██║██║
            ██║  ██╗██║  ██║╚██████╔╝╚█████╔╝██║
            ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝
                                                

                
    This script get all previous bitmoji's and save in a directory named by username
    """
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-u", "--Username", help = "To Query the Username")
    args = parser.parse_args()
    if args.Username:
        func(args.Username)