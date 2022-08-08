# This will not run on online IDE
# pylint: disable=invalid-name
# pylint: disable=consider-using-enumerate
import json
from operator import contains
import requests
from nfl_scraper.nfl_models import Game, League
from nfl_scraper.nfl_models import Team
from nfl_scraper.nfl_models import Championship
from nfl_scraper.nfl_models import Season
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#TODO VERY HIGH Move the models up to be shared
#TODO HIGH Add Output(json|excel) method to models
#TODO MED Make these inputs
#TODO LOW Organize the methods a little better
#TODO VERY LOW I sort of want to utilize the objects in a web app for data manipulation/query
USERNAME = "myemail@gmail.com"
PASSWORD = "mypassword"
LEAGUE_ID = "123456"
#This name isnt' used for matching, so it can be anythin
LEAGUE_NAME = "MileHigh"
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
    email.send_keys(USERNAME)
    passw = driver.find_element("xpath","//input[@type='password']")
    passw.send_keys(PASSWORD)
    button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Sign In button']")))
    button.click()
    league = League(LEAGUE_NAME, LEAGUE_ID)
    driver.implicitly_wait(5)
    print(driver.title)
    URL = f"https://fantasy.nfl.com/league/{league.id}/history"
    driver.get(URL)
    ships(driver, league)
    single_game_points(driver, league)
    single_player_points_leader(driver, league)
    points_leader(driver, league)
    add_teams_to_seasons(driver, league)
    get_schedules_and_rosters(driver, league)
    add_playoffs(driver, league)
    driver.implicitly_wait(5)
    
def ships(driver, league):
    winner_rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div[1]/table/tbody/tr")
    print("found")
    print(str(len(winner_rows)))
    for x in range(len(winner_rows)):
        year = winner_rows[x].find_element("xpath",".//td[1]").text
        team = get_team(winner_rows[x], "3", [])
        ship = Championship(year)
        team.add_ship(ship)
        season = Season(year, team)
        league.update_season(season)
        print(f"Year:{year} Name:{team.name} Id:{team.id}")
    print(driver.title)
    
def single_game_points(driver, league):
    winner_rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr")
    print("found")
    print(str(len(winner_rows)))
    for x in range(len(winner_rows)):
        year = winner_rows[x].find_element("xpath",".//td[1]").text
        week = winner_rows[x].find_element("xpath",".//td[2]").text
        points = winner_rows[x].find_element("xpath",".//td[4]").text
        season = league.seasons[year]
        team = get_team(winner_rows[x], "3", season)
        season.set_highest_score(team.id, points, week)
        league.update_season(season)
        print(f"Team:{team.name} Week:{season.highest_score_week} Score:{season.highest_score}")
    print(driver.title)

def get_schedules_and_rosters(driver, league):
    for year in league.seasons:
        season = league.seasons[year]
        for teamid in season.teams:
            url = "https://fantasy.nfl.com/league/"+league.id+"/history/"+season.year+"/schedule?standingsTab=schedule&scheduleType=team&leagueId="+league.id+"&scheduleDetail="+teamid
            driver.get(url)
            driver.implicitly_wait(3)
            team = season.teams[teamid]
            game_rows = driver.find_element("xpath", "/table/tbody/tr")
            for x in range(len(game_rows)):
                game_row = game_rows[x]
                week = game_row.find_element("xpath", ".//td[1]").text
                opp_team = get_team(game_row, "2", season)
                score = game_row.find_element("xpath", ".//td[3]/a/em[1]").text
                opponent_score = game_row.find_element("xpath", ".//td[3]/a/em[2]").text
                team.add_game(Game(week, team.name, team.id, score, opp_team.id, opp_team.name, opponent_score))

def single_player_points_leader(driver, league):
    winner_rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div[3]/table/tbody/tr")
    print("found")
    print(str(len(winner_rows)))
    for x in range(len(winner_rows)):
        year = winner_rows[x].find_element("xpath",".//td[1]").text
        week = winner_rows[x].find_element("xpath",".//td[2]").text
        points = winner_rows[x].find_element("xpath",".//td[5]").text
        player_name = winner_rows[x].find_element("xpath",".//td[4]/div/a").text
        player_pos_team = winner_rows[x].find_element("xpath",".//td[4]/div/em").text
        season = league.seasons[year]
        team = get_team(winner_rows[x], "3", season)
        season.set_highest_player_score(team.id, points, week, player_name, player_pos_team)
        league.update_season(season)
        print(f"Team:{team.name} Week:{week} Score:{points} PlayerName: {player_name} PlayerPos: {player_pos_team}")
    print(driver.title)


def points_leader(driver, league):
    winner_rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div[4]/table/tbody/tr")
    print("found")
    print(str(len(winner_rows)))
    for x in range(len(winner_rows)):
        year = winner_rows[x].find_element("xpath",".//td[1]").text
        points = winner_rows[x].find_element("xpath",".//td[4]").text
        season = league.seasons[year]
        team = get_team(winner_rows[x], "3", season)
        
        season.set_points_leader(team.id, points)
        league.update_season(season)
        print(f"Team:{team.name} Score:{season.highest_score}")
    print(driver.title)

def add_playoffs(driver, league):
    for year in league.seasons:
        season = league.seasons[year]
        url = "https://fantasy.nfl.com/league/"+league.id+"/history/"+year+"/playoffs"
        driver.get(url)
        playoff_weeks = driver.find_elements("xpath","/ul[@class='playoffContent']/li")
        for x in range(len(playoff_weeks)):
            playoff_week = playoff_weeks[x]
            week = playoff_week.find_element("xpath", ".//li[1]/h4").text.remove("Week").strip()
            team_row = playoff_week.find_elements("xpath", ".//li[1]/div[1]")
            team = get_team(team_row, "1", season, container = "div")
            score = team_row.find_element("xpath", ".//li[1]/div[1]/div[2]").text
            opp_team_row = playoff_week.find_elements("xpath", ".//li[1]/div[2]")
            opp_team = get_team(opp_team_row, "1", season, container = "div")
            opp_score = opp_team_row.find_element("xpath", ".//li[1]/div[1]/div[2]").text
            playoff_game = Game(week, team.name, team.id, score, opp_team.name, opp_team.id, opp_score)
            season.add_playoff_game(playoff_game)
        league.update_season(season)

def add_teams_to_seasons(driver, league):
    for year in league.seasons:
        season = league.seasons[year]
        url = "https://fantasy.nfl.com/league/"+league.id+"/history/"+year+"/standings?historyStandingsType=regular"
        count_divisions = -1
        driver.get(url)
        driver.implicitly_wait(3)
        try:
            divisions = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[5]/div/div/div[contains(@class,'hasDivisions')]")
            count_divisions = len(divisions) - 1
            if count_divisions == -1:
                count_divisions = 1
        except Exception:
            print("add_teams_to_seasons potential error: "+year)
        
        for division_index in range(count_divisions):
            if count_divisions == 1:
                rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[5]/div/div/div[1]/table/tbody/tr")
                division = ""
            else:
                #Selenium doesn't zero index..gross
                rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[5]/div/div/div["+str(division_index+2)+"]/table/tbody/tr")
                division = driver.find_element("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[5]/div/div/div["+str(division_index+2)+"]/h5").text.split(':')[1].strip()
            team_count = len(rows)
            print("current teams: " +str(len(season.teams)))
            for x in range(team_count):
                record = rows[x].find_element("xpath",".//td[3]").text
                points_for = rows[x].find_element("xpath",".//td[6]").text
                points_against = rows[x].find_element("xpath",".//td[7]").text
                team = get_team(rows[x], "2", season)
                if team.id in season.teams:
                    team = season.teams[team.id]
                team.add_record(record, points_for, points_against, division)
                season.teams[team.id] = team
                print(f"Team:{team.name} Points for: {points_for} Points Against:{points_against} Record: {record}")
            league.update_season(season)
        print(driver.title)


def get_team(row, col, season, container = "td"):
    """Pulling the team name and id out of the expected column

    Args:
        row (_type_): _description_
        col (_type_): _description_
        season (_type_): _description_

    Returns:
        _type_: _description_
    """
    team_a = row.find_element("xpath",".//"+container+"["+col+"]/div/a[2]")
    team_id = team_a.get_attribute("href").split('/')[-1]
    # Into earlier seasons the urls were a bit different
    if "teamId=" in team_id:
        team_id = team_id.split('teamId=')[1]
    try:
        return season.teams[team_id]
    except Exception:
        return Team(team_id, team_a.text)



def main_page():  
    URL = "https://id.nfl.com/account/sign-in?authReturnUrl=https%3A%2F%2Fid.nfl.com%2Faccount"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(url=URL, headers=headers)
    #r = requests.get(URL)
    
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    print(soup.prettify())
    # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.




#curl 'https://auth-id.nfl.com/accounts.login' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://id.nfl.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: https://id.nfl.com/' -H 'Cookie: minUnifiedSessionToken10=%7B%22sessionId%22%3A%227fbe64aec5-95719cccf2-313b701e05-b193b6bb29-a408a2296f%22%2C%22uid%22%3A%22ccb831a28f-ee1bf88e61-5958c2541b-f07840b5c6-48c46ce71b%22%2C%22__sidts__%22%3A1659327116035%2C%22__uidts__%22%3A1659327116035%7D; AMCV_F75C3025512D2C1D0A490D44%40AdobeOrg=1176715910%7CMCIDTS%7C19206%7CMCMID%7C55261168582936950933385932010619879756%7CMCAID%7CNONE%7CMCOPTOUT-1659334477s%7CNONE%7CvVersion%7C5.4.0; mbox=session#c7bf6c244f08423db36af9c72c7dd0b5#1659328992; at_check=true; _gcl_au=1.1.1348799463.1659327116; s_ecid=MCMID%7C55261168582936950933385932010619879756; AMCVS_F75C3025512D2C1D0A490D44%40AdobeOrg=1; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.nfl.com/%22%2C%22sref%22:%22%22%2C%22sts%22:1659327117033%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=24c6c2a56c3c2c97def3a9225180f85e%22%2C%22session_count%22:1%2C%22last_session_ts%22:1659327117033}; s_pv=nfl.com%3Aaccount%3Aaccount%3Asign%20in; s_ptc=pt.rdr%240.00%5E%5Ept.apc%240.02%5E%5Ept.dns%240.94%5E%5Ept.tcp%240.04%5E%5Ept.req%240.05%5E%5Ept.rsp%240.00%5E%5Ept.prc%243.12%5E%5Ept.onl%240.00%5E%5Ept.tot%244.24%5E%5Ept.pfi%241; s_cc=true; gmid=gmid.ver4.AcbHWfOm-g.JwjuHiKemX_YpnBfV4oGc4lmJy-yQWvGa6c1Wzdu-tvm86UI68MSgqWHKNhFnDmS.zTG8KowiK2ljPM6tHQj_jgVg40jDEspnbTcGbQDaDgPJVxS1Z2iYfixquD66-4Zj8P4PWQhUi_KDMtOE4xjhrQ.sc3; ucid=hYJGSkBsIINlJE9GISayag; hasGmid=ver4; gig_bootstrap_3_Qa8TkWpIB8ESCBT8tY2TukbVKgO5F6BJVc7N1oComdwFzI7H2L9NOWdm11i_BY9f=auth-id_ver4; gig_canary_3_h1AiUI9kcBduMJ2JoYPP6EXq3FGIy75RiS2DqkxjARGPcVazXVlNcGAOhgAfrU0P=false; gig_canary_ver_3_h1AiUI9kcBduMJ2JoYPP6EXq3FGIy75RiS2DqkxjARGPcVazXVlNcGAOhgAfrU0P=13318-3-27655425; apiDomain_3_h1AiUI9kcBduMJ2JoYPP6EXq3FGIy75RiS2DqkxjARGPcVazXVlNcGAOhgAfrU0P=auth-id.nfl.com; gig_bootstrap_3_3g_DApOD0TCeN6ZJpzQMr7H1cIbtqtHwDjKVESN3N5oohMleIozT0I9WecPZeytT=auth-id_ver4; gig_canary_ver=13318-3-27655425' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'TE: trailers' --data-raw 'loginID=shanechambers85%40gmail.com&password=Sn0wb0ard%40Abay1&sessionExpiration=0&targetEnv=jssdk&include=profile%2Cdata&includeUserInfo=true&lang=en&APIKey=3_3g_DApOD0TCeN6ZJpzQMr7H1cIbtqtHwDjKVESN3N5oohMleIozT0I9WecPZeytT&sdk=js_latest&authMode=cookie&pageURL=https%3A%2F%2Fid.nfl.com%2Faccount&sdkBuild=13318&format=json'




