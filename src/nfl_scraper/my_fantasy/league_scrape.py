# pylint: disable=invalid-name
# pylint: disable=consider-using-enumerate

import requests
from utils.ff_models import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jsonpickle

VERBOSE = True
def debug_print(message):
    """_summary_

    Args:
        message (_type_): _description_
    """
    if VERBOSE is True:
        print(message)

def get_driver():
    """_summary_

    Returns:
        _type_: _description_
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    #options.add_argument('--headless')
    return webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)

def get(year, leagueid, name, verbose) -> None:
    """Running this will run the entirety of the scrap. I've been using the debugger in 
    vscode
    """
    VERBOSE=verbose
    driver = get_driver()
    debug_print(driver.title)
    league = League(name, leagueid)
    URL = f"https://www98.myfantasyleague.com/{year}/home/{leagueid}"
    driver.get(URL)
    #ships(driver, league)
    #single_game_points(driver, league)
    #single_player_points_leader(driver, league)
    #points_leader(driver, league)
    add_teams_to_seasons(driver, league)
    get_schedules_and_rosters(driver, league)
    with open("league_"+league.id+".json", "w") as write_file:
        write_file.write(str(jsonpickle.encode(league)))
    #TODO: Getting a key error with adding playoffs. Need to revisit.
    #The playoff games are recorded as part of the schedule above, so
    #technically, you could do some calculations on when the playoffs
    #started and track a team through playoff games, and record validation
    #until this is fixed, the game_types won't distinguish between playoff
    #and consolation games in  post season.
    #add_playoffs(driver, league)
    with open("league_"+league.id+".json", "w") as write_file:
        write_file.write(str(jsonpickle.encode(league)))

def add_teams_to_seasons(driver, league) -> None:
    """Adding the teams individually to a season

    Args:
        driver (_type_): _description_
        league (_type_): _description_
    """
    count_divisions = -1
    #driver.implicitly_wait(3)
    try:
        divisions = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[5]/div/div/div[contains(@class,'hasDivisions')]")
        count_divisions = len(divisions) - 1
        if count_divisions == -1:
           count_divisions = 1
    except Exception:
        debug_print("add_teams_to_seasons potential error: "+year)
        
    for division_index in range(count_divisions):
        if count_divisions == 1:
                rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[5]/div/div/div[1]/table/tbody/tr")
                division = ""
            else:
                #Selenium doesn't zero index..gross
                rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[5]/div/div/div["+str(division_index+2)+"]/table/tbody/tr")
                division = driver.find_element("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[5]/div/div/div["+str(division_index+2)+"]/h5").text.split(':')[1].strip()
            team_count = len(rows)
            debug_print("current teams: " +str(len(season.teams)))
            for x in range(team_count):
                rank = rows[x].find_element("xpath",".//td[1]").text
                record = rows[x].find_element("xpath",".//td[3]").text
                points_for = rows[x].find_element("xpath",".//td[6]").text
                points_against = rows[x].find_element("xpath",".//td[7]").text
                team = get_team(rows[x], "2", season)
                if team.id in season.teams:
                    team = season.teams[team.id]
                team.add_record(record, points_for, points_against, rank, division)
                season.teams[team.id] = team
                debug_print(f"Team:{team.name} Points for: {points_for} Points Against:{points_against} Record: {record}")
            league.update_season(season)
        debug_print(driver.title)
