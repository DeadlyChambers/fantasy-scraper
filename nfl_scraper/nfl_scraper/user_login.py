#This will not run on online IDE
import requests
from bs4 import BeautifulSoup

def main_page():  
    URL = "https://id.nfl.com/account/sign-in?authReturnUrl=https%3A%2F%2Fid.nfl.com%2Faccount"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(url=URL, headers=headers)
    #r = requests.get(URL)
    
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    print(soup.prettify())
    # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.









