import os,shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests,base64
import argparse
import img2pdf
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
    
    initURL="https://www.snapchat.com/add/"+username
    if os.path.exists(username):
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
                
    os.chdir(username)
    images = [i for i in os.listdir(os.getcwd()) if i.endswith(".jpg")]
    dpix = dpiy = 300
    layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
    
    with open("../"+username+".pdf", "wb") as f:
        f.write(img2pdf.convert(images,layout_fun=layout_fun))
    os.chdir("../")
    shutil.rmtree(username, ignore_errors=False)
    driver.close()
    print("\t\t\tThank you for using khoji")
    print("\t\t\tPrevious Bitmoji's count is "+str(count))
    print("\t\t\tPrevious Bitmoji's of "+username+" are saved in "+username+".pdf")
    
if __name__== "__main__":
    description = """

            ██╗  ██╗██╗  ██╗ ██████╗      ██╗██╗
            ██║ ██╔╝██║  ██║██╔═══██╗     ██║██║
            █████╔╝ ███████║██║   ██║     ██║██║
            ██╔═██╗ ██╔══██║██║   ██║██   ██║██║
            ██║  ██╗██║  ██║╚██████╔╝╚█████╔╝██║
            ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝
                                                
    This script get all previous bitmoji's and save in a pdf file named by username.pdf
    """
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-u", "--Username", help = "To Query the Username")
    args = parser.parse_args()
    if args.Username:
        func(args.Username)