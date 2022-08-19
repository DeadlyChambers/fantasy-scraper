# This will not run on online IDE
# pylint: disable=invalid-name
# pylint: disable=consider-using-enumerate
from operator import contains
import requests
from utils.ff_models import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jsonpickle


#TODO HIGH Add Output(json|excel) #json is done, but not part of a method
#TODO MED Make username, password, league id as inputs to module call
#TODO LOW Organize the methods a little better
#TODO VERY LOW I sort of want to utilize the objects in a web app for data manipulation/query

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
    return webdriver.Chrome(chrome_options=options)

def open_main_page(username, password, leagueid, name, verbose) -> None:
    """Running this will run the entirety of the scrap. I've been using the debugger in 
    vscode
    """
    VERBOSE=verbose
    driver = get_driver()
    URL = "https://id.nfl.com/account/sign-in"
    driver.get(URL)
    debug_print(driver.title)
    driver.find_element("xpath","//input[@type='email']").send_keys(username)
    driver.find_element("xpath","//input[@type='password']").send_keys(password)
    button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Sign In button']")))
    button.click()
    league = League(name, leagueid)
    driver.implicitly_wait(3)
    debug_print(driver.title)
    URL = f"https://fantasy.nfl.com/league/{league.id}/history"
    driver.get(URL)
    ships(driver, league)
    single_game_points(driver, league)
    single_player_points_leader(driver, league)
    points_leader(driver, league)
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

    
def ships(driver, league) -> None:
    """What it is all about, yachts and champagne

    Args:
        driver (_type_): _description_
        league (_type_): _description_
    """
    winner_rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div[1]/table/tbody/tr")
    debug_print("found")
    debug_print(str(len(winner_rows)))
    for x in range(len(winner_rows)):
        year = winner_rows[x].find_element("xpath",".//td[1]").text
        team = get_team(winner_rows[x], "3", [])
        ship = Championship(year)
        team.add_ship(ship)
        season = Season(year, team)
        league.update_season(season)
        debug_print(f"Year:{year} Name:{team.name} Id:{team.id}")
    debug_print(driver.title)
    
def single_game_points(driver, league) -> None:
    """Season Single Game Point Scoring leader

    Args:
        driver (_type_): _description_
        league (_type_): _description_
    """
    winner_rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr")
    debug_print("found")
    debug_print(str(len(winner_rows)))
    for x in range(len(winner_rows)):
        year = winner_rows[x].find_element("xpath",".//td[1]").text
        week = winner_rows[x].find_element("xpath",".//td[2]").text
        points = winner_rows[x].find_element("xpath",".//td[4]").text
        season = league.seasons[year]
        team = get_team(winner_rows[x], "3", season)
        season.set_highest_score(team.id, points, week)
        league.update_season(season)
        debug_print(f"Team:{team.name} Week:{season.highest_score_week} Score:{season.highest_score}")
    debug_print(driver.title)

def get_schedules_and_rosters(driver, league) -> None:
    """Adding each game directly to the individual team. It would be where
    I'd probably add rosters, but not messing with it atm

    Args:
        driver (_type_): _description_
        league (_type_): _description_
    """
    for year in league.seasons:
        season = league.seasons[year]
        for teamid in season.teams:
            #&gameSeason=year
            url = "https://fantasy.nfl.com/league/"+league.id+"/history/"+year+"/schedule?standingsTab=schedule&scheduleType=team&leagueId="+league.id+"&scheduleDetail="+teamid
            driver.get(url)
            #driver.implicitly_wait(2)
            team = season.teams[teamid]
            #Could pull userId from class, unless the user no longer exists
            team.set_manager(driver.find_element("xpath", "//a[contains(@class,'userName')]").text)
            #Currently the only table on page, trying out the //
            game_rows = driver.find_elements("xpath", "//table/tbody/tr")
            for x in range(len(game_rows)):
                try:
                    week = game_rows[x].find_element("xpath", ".//td[1]").text
                    opp_team = get_team(game_rows[x], "2", season)
                    score = game_rows[x].find_element("xpath", ".//td[3]/div/a/em[1]").text
                    opponent_score = game_rows[x].find_element("xpath", ".//td[3]/div/a/em[2]").text
                    debug_print(f"{team.name} vs {opp_team.name} was {score}-{opponent_score}")
                    team.add_game(Game(week, team.name, team.id, score, opp_team.id, opp_team.name, opponent_score, "regular"))
                except Exception:
                    #Honestly this is sort of a guess, it happens in playoffs
                    team.add_bye_week(game_rows[x].find_element("xpath", ".//td[1]").text)

def single_player_points_leader(driver, league) -> None:
    """I planned on added players, but it felt like overkill. At least each season point
    scorer is recorded to the season

    Args:
        driver (_type_): _description_
        league (_type_): _description_
    """
    winner_rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div[3]/table/tbody/tr")
    debug_print("found")
    debug_print(str(len(winner_rows)))
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
        debug_print(f"Team:{team.name} Week:{week} Score:{points} PlayerName: {player_name} PlayerPos: {player_pos_team}")
    debug_print(driver.title)


def points_leader(driver, league) -> None:
    """Points leader is a single team each season..unless there is a tie then
    this is f'd

    Args:
        driver (_type_): _description_
        league (_type_): _description_
    """
    winner_rows = driver.find_elements("xpath","/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div[4]/table/tbody/tr")
    debug_print("found")
    debug_print(str(len(winner_rows)))
    for x in range(len(winner_rows)):
        year = winner_rows[x].find_element("xpath",".//td[1]").text
        points = winner_rows[x].find_element("xpath",".//td[4]").text
        season = league.seasons[year]
        team = get_team(winner_rows[x], "3", season)
        season.set_points_leader(team.id, points)
        league.update_season(season)
        debug_print(f"Team:{team.name} Score:{season.highest_score}")
    debug_print(driver.title)

def add_playoffs(driver, league) -> None:
    """The playoffs are weird animal so made it an array of games on the season,
    and added the games to each team that played in them. Could mess up something with
    teams having exta games. Adding a boolean for isPlayoffs if that distinction needs
    to be made

    Args:
        driver (_type_): _description_
        league (_type_): _description_
    """
    for year in league.seasons:
        season = league.seasons[year]
        url = "https://fantasy.nfl.com/league/"+league.id+"/history/"+year+"/playoffs"
        driver.get(url)
        playoff_weeks = driver.find_elements("xpath","//ul[@class='playoffContent']/li")
        for x in range(len(playoff_weeks)):
            week = playoff_weeks[x].find_element("xpath", ".//h4").text.replace("Week", "").strip()
            playoff_games = playoff_weeks[x].find_elements("xpath", ".//ul/li")
            for y in range(len(playoff_games)):
                week_title = playoff_games[y].find_element("xpath", ".//h5").text.strip()
                game_type = "consolation" if "final" not in week_title or "Bowl" not in week_title else "playoff"
                #playoff_games[y].find_element("xpath", ".//div/")
                team = get_team_from_a(playoff_games[y].find_element("xpath", ".//div/div[1]/div[1]/a"), season)
                score = playoff_games[y].find_element("xpath", ".//div/div[1]/div[2]").text
                opp_team = get_team_from_a(playoff_games[y].find_element("xpath", ".//div/div[2]/div[1]/a"), season)
                opp_score = playoff_games[y].find_element("xpath", ".//div/div[2]/div[2]").text
                playoff_game = Game(week, team.name, team.id, score, opp_team.id, opp_team.name, opp_score, game_type)
                season.add_playoff_game(playoff_game)
                debug_print(f"{team.name} vs {opp_team.name} was {score}-{opp_score}")
            #TODO: Consider ensuring any other games not in playoffs set as toilet bowl or something
        league.update_season(season)

def add_teams_to_seasons(driver, league) -> None:
    """Adding the teams individually to a season

    Args:
        driver (_type_): _description_
        league (_type_): _description_
    """
    for year in league.seasons:
        season = league.seasons[year]
        url = "https://fantasy.nfl.com/league/"+league.id+"/history/"+year+"/standings?historyStandingsType=regular"
        count_divisions = -1
        driver.get(url)
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


def get_team(row, col, season, container = "td") -> Team:
    """Pulling the team name and id out of the expected column

    Args:
        row (_type_): _description_
        col (_type_): _description_
        season (_type_): _description_

    Returns:
        _type_: _description_
    """
    team_a = row.find_element("xpath",".//"+container+"["+col+"]/div/a[2]")
    return get_team_from_a(team_a, season)

def get_team_from_a(atag, season) -> Team:
    """_summary_

    Args:
        atag (_type_): _description_
        season (_type_): _description_

    Returns:
        _type_: _description_
    """
    team_id = atag.get_attribute("href").split('/')[-1]
    # Into earlier seasons the urls were a bit different
    if "teamId=" in team_id:
        team_id = team_id.split('teamId=')[1]
    try:
        return season.teams[team_id]
    except Exception:
        return Team(team_id, atag.text)

def main_page() -> None:
    """_summary_
    """
    URL = "https://id.nfl.com/account/sign-in?authReturnUrl=https%3A%2F%2Fid.nfl.com%2Faccount"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(url=URL, headers=headers)
    #r = requests.get(URL)
    
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    debug_print(soup.prettify())
    # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.
