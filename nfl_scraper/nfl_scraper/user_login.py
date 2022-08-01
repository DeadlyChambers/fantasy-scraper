#This will not run on online IDE
from time import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = "myemail@email.com"
password = "yourpassword"
leagueid = "372821"
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    #options.add_argument('--headless')
    return webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)
    

def open_main_page():
    driver = get_driver()
    URL = "https://id.nfl.com/account/sign-in"
    driver.get(URL)
    print(driver.title)
    email = driver.find_element("xpath","//input[@type='email']")
    email.send_keys(username)
    passw = driver.find_element("xpath","//input[@type='password']")
    passw.send_keys(password)
    button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Sign In button']")))
    button.click()
    
    driver.implicitly_wait(5)
    print(driver.title)
    almanac(driver, leagueid)
    driver.implicitly_wait(5)
    #page_source = driver.page_source
    #soup = BeautifulSoup(page_source, 'html5lib')
    #print(soup.prettify())
    
def almanac(driver, league_id):
    URL = f"https://fantasy.nfl.com/league/{league_id}/history"
    driver.get(URL)
    #league champ
    winner_tables = driver.find_elements("xpath","//table[@class='tableType-history hasGroups']")
    print(str(len(winner_tables)))
    #for y in range(len(winner_tables)):
    #table_text = winner_tables[0].get_attribute('innerHTML')
    
    #winner_rows = winner_tables[0].get().childNodes().find_elements("xpath","/tbody//tr")
    winner_rows = winner_tables[0].find_elements("xpath","//table[@class='tableType-history hasGroups'][0]/tbody//tr")
    print("found")
    print(str(len(winner_rows)))
    for x in range(len(winner_rows)):
        year_el = driver.find_element("xpath",f"//table[@class='tableType-history hasGroups'][1]/tbody//tr[{x}]/td[1]")
        year = year_el.text
        team_a = driver.find_element("xpath",f"//table[@class='tableType-history hasGroups'][1]/tbody//tr[{x}]/td[3]/a[contains(@class, 'teamName')]")
        team_name = team_a.text
        team_id = team_a.getAttribute("href").spilt('/')[-1]
        print(f"Year:{year} Name:{team_name} Id:{team_id}")
    # print(table_text)
    # table = BeautifulSoup(table_text, features="html5lib")
    # print(table.prettify())
    # #table = tables.find_all("table")[0]
    # #TODO figure out how loop over the winner_tables
    # rows = table.find_all({"tbody", "tr"})
    # print(str(len(rows)))
    # for row in range(len(rows)):
    #     cells = rows.index(row).find("td")
    #     print(str(len(cells)))
    #     year = cells[0].get_text()
    #     team_a = cells[2]
    #     team_name = team_a.get_text()
    #     team_id = team_a.get_attribute("href").spilt('/')[-1]
    #     print(f"Year:{year} Name:{team_name} Id:{team_id}")
    # winner_rows = winner_tables[1].find_elements("xpath","/tbody//tr")
    # print("found")
    # print(str(len(winner_rows)))
    # for x in range(len(winner_rows)):
        
    #     year_el = driver.find_element("xpath",f"//table[@class='tableType-history hasGroups'][1]/tbody//tr[{x}]/td[1]")
    #     year = year_el.text
    #     team_a = driver.find_element("xpath",f"//table[@class='tableType-history hasGroups'][1]/tbody//tr[{x}]/td[3]/a[contains(@class, 'teamName')]")
    #     team_name = team_a.text
    #     team_id = team_a.getAttribute("href").spilt('/')[-1]
    #     print(f"Year:{year} Name:{team_name} Id:{team_id}")
    print(driver.title)
    



def main_page():  
    URL = "https://id.nfl.com/account/sign-in?authReturnUrl=https%3A%2F%2Fid.nfl.com%2Faccount"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(url=URL, headers=headers)
    #r = requests.get(URL)
    
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    print(soup.prettify())
    # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.




#curl 'https://auth-id.nfl.com/accounts.login' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://id.nfl.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: https://id.nfl.com/' -H 'Cookie: minUnifiedSessionToken10=%7B%22sessionId%22%3A%227fbe64aec5-95719cccf2-313b701e05-b193b6bb29-a408a2296f%22%2C%22uid%22%3A%22ccb831a28f-ee1bf88e61-5958c2541b-f07840b5c6-48c46ce71b%22%2C%22__sidts__%22%3A1659327116035%2C%22__uidts__%22%3A1659327116035%7D; AMCV_F75C3025512D2C1D0A490D44%40AdobeOrg=1176715910%7CMCIDTS%7C19206%7CMCMID%7C55261168582936950933385932010619879756%7CMCAID%7CNONE%7CMCOPTOUT-1659334477s%7CNONE%7CvVersion%7C5.4.0; mbox=session#c7bf6c244f08423db36af9c72c7dd0b5#1659328992; at_check=true; _gcl_au=1.1.1348799463.1659327116; s_ecid=MCMID%7C55261168582936950933385932010619879756; AMCVS_F75C3025512D2C1D0A490D44%40AdobeOrg=1; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.nfl.com/%22%2C%22sref%22:%22%22%2C%22sts%22:1659327117033%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=24c6c2a56c3c2c97def3a9225180f85e%22%2C%22session_count%22:1%2C%22last_session_ts%22:1659327117033}; s_pv=nfl.com%3Aaccount%3Aaccount%3Asign%20in; s_ptc=pt.rdr%240.00%5E%5Ept.apc%240.02%5E%5Ept.dns%240.94%5E%5Ept.tcp%240.04%5E%5Ept.req%240.05%5E%5Ept.rsp%240.00%5E%5Ept.prc%243.12%5E%5Ept.onl%240.00%5E%5Ept.tot%244.24%5E%5Ept.pfi%241; s_cc=true; gmid=gmid.ver4.AcbHWfOm-g.JwjuHiKemX_YpnBfV4oGc4lmJy-yQWvGa6c1Wzdu-tvm86UI68MSgqWHKNhFnDmS.zTG8KowiK2ljPM6tHQj_jgVg40jDEspnbTcGbQDaDgPJVxS1Z2iYfixquD66-4Zj8P4PWQhUi_KDMtOE4xjhrQ.sc3; ucid=hYJGSkBsIINlJE9GISayag; hasGmid=ver4; gig_bootstrap_3_Qa8TkWpIB8ESCBT8tY2TukbVKgO5F6BJVc7N1oComdwFzI7H2L9NOWdm11i_BY9f=auth-id_ver4; gig_canary_3_h1AiUI9kcBduMJ2JoYPP6EXq3FGIy75RiS2DqkxjARGPcVazXVlNcGAOhgAfrU0P=false; gig_canary_ver_3_h1AiUI9kcBduMJ2JoYPP6EXq3FGIy75RiS2DqkxjARGPcVazXVlNcGAOhgAfrU0P=13318-3-27655425; apiDomain_3_h1AiUI9kcBduMJ2JoYPP6EXq3FGIy75RiS2DqkxjARGPcVazXVlNcGAOhgAfrU0P=auth-id.nfl.com; gig_bootstrap_3_3g_DApOD0TCeN6ZJpzQMr7H1cIbtqtHwDjKVESN3N5oohMleIozT0I9WecPZeytT=auth-id_ver4; gig_canary_ver=13318-3-27655425' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'TE: trailers' --data-raw 'loginID=shanechambers85%40gmail.com&password=Sn0wb0ard%40Abay1&sessionExpiration=0&targetEnv=jssdk&include=profile%2Cdata&includeUserInfo=true&lang=en&APIKey=3_3g_DApOD0TCeN6ZJpzQMr7H1cIbtqtHwDjKVESN3N5oohMleIozT0I9WecPZeytT&sdk=js_latest&authMode=cookie&pageURL=https%3A%2F%2Fid.nfl.com%2Faccount&sdkBuild=13318&format=json'




